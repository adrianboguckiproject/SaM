# SOLUTION


# cloud
we can use a Cloud Functions, triggered by Runtime

Add Scheduler Trigger 

# my solution (based on docker)

Mongo DB that get NOSQL data (jason packed)

where data is stored in full JSON
[
    {"data":
        {"EUR":1,"PLN":4.2578922829,"USD":1.0866847229},
    "date":"2024-05-17",
    "source":"freecurrency"
    }
]

we need cron job, to run this app(optionaly docker container) everyday


# EXECUTION

dockerized, before run flask, please run docker compose up
and wait till mongodb will start

db should be discovered automatically on localhost (if you have a docker)


in main folder in CMD run:
 pip install -r req.txt
 python -m flask run

# Emergecy URL activation
http://localhost:5000/emergecy_retrieve

# Need more performance?
We can create index on date 

# There is no downloading historical data


