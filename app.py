import json
from datetime import datetime

import pymongo
from bson import json_util

from flask import Flask
import freecurrencyapi
from pymongo import MongoClient


app = Flask(__name__)


def get_older_data(base_reporting_currency, currency, collection):

    rate = None
    currency_value = collection.find().sort([("date", pymongo.ASCENDING)])
    for e in currency_value:
        if (
            e["date"] < str(datetime.utcnow().date())
            and e["data"][currency] is not None and e["base_reporting_currency"] == base_reporting_currency
        ):
            rate = e["data"][currency]

    return rate


def get_data_from_freecurrencyapi(base_reporting_currency, currencies, collection):
    client = freecurrencyapi.Client("fca_live_dRh5gtBO3OPolW9X8RDAY7yazjCWM4x4QDkPFShK")
    query = client.latest(base_currency=base_reporting_currency, currencies=currencies)
    query["base_reporting_currency"] = base_reporting_currency
    for currency in currencies:
        if not query["data"][currency]:
            result = get_older_data(base_reporting_currency, currency, collection)
            query["data"][currency] = result

    return query

def check_duplicate(base_reporting_currency, collection):
    duplicates= list(collection.find({ "base_reporting_currency": base_reporting_currency, "date": str(datetime.now().date()) }).sort([("date", pymongo.ASCENDING)]))
    print('Duplicates:',duplicates)
    if len(duplicates) > 0:
        print("Duplicate found")
        return True
    return False

def get_data_from_external_sources(base_reporting_currency, currencies, source_type, collection):
    if source_type == "freecurrency":
        retrieved_data = get_data_from_freecurrencyapi(base_reporting_currency, currencies, collection)
    retrieved_data["date"] = str(datetime.now().date())
    if check_duplicate(base_reporting_currency, collection):
        return {}
    retrieved_data["source"] = source_type
    return retrieved_data


def connect_to_mongo():
    connection_string = "mongodb://root:pass@localhost"
    client = MongoClient(connection_string)
    return client["exchange_db"]


def insert_list(list_of_inserts, collection):
    for element in list_of_inserts:
        json_object = json.loads(json_util.dumps(element, indent=4))
        collection.insert_one(json_object)


def start_app(base_reporting_currency = "EUR", currencies_we_want = ["EUR", "USD", "PLN", "CHF"]):  # put application's code here

    api_sources = [
        "freecurrency",
    ]

    db_name = connect_to_mongo()
    collection_name = db_name["euro_exchange_rate"]

    result = []
    for source in api_sources:
        result.append(
            get_data_from_external_sources(base_reporting_currency, currencies_we_want, source, collection_name)
        )

    insert_list(result, collection_name)
    print('Added ', result)
    return "Finished, added data: " + str(result), 200


@app.route("/emergecy_retrieve")
def emergecy_retrieve():
    return start_app()


if __name__ == "__main__":
    app.run(debug=True)
start_app()
