# RateLimit Example

## Installing and running

This example was written in Python 3.5.2. Steps to install:

* Clone repository.
* Get into the cloned repo: `cd ratelimitpy`
* Create a virtual environment: `pyvenv-3.5 env` 
* Activate it: `. ./env/bin/activate`
* Install: `pip install .`
* Run: `FLASK_APP=ratelimitpy flask run`
* Hit with requests: `curl -H 'Authorization: Bearer potato' 'http://127.0.0.1:5000/hotels?city=Bangkok&asc=false'`

## Assumptions made

Here is a list of assumptions I've made while doing this assignment:

* The assignment talks about city id but I only found city name in the csv, so the search is by city name.
* The token bucket allows bursts of the number of requests you say per second. So if you say one request per 2 seconds, it allows only one request as a burst.
* When you're banned you have to wait the ban time and you're not penalized for trying again.
* The configuration for rate limit is for all endpoints.
* Python supports threads and it is common in production configurations to use them. It is true that only one thread runs at a time in python, but it can stop in the middle of something critical, that's why you will find locks in two critical areas of shared data.
* There are some unit and not so unit tests for the file database and rate limit functionality. You can run them after installing pytest with `pytest`.
* And for sure the quesiton of why python? It is easy to prototype functionality.
