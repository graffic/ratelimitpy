# RateLimit Example

[![Build Status](https://travis-ci.org/graffic/ratelimitpy.svg?branch=master)](https://travis-ci.org/graffic/ratelimitpy)
[![Coverage Status](https://coveralls.io/repos/github/graffic/ratelimitpy/badge.svg?branch=master)](https://coveralls.io/github/graffic/ratelimitpy?branch=master)

## Assignment description

You are provided with hotels database in CSV (Comma Separated Values) format.
We need you to implement HTTP service, according to the API requirements described below. You may use any language or platform that you like: C#/Java/Scala/etc.

1.  RateLimit: API calls need to be rate limited (request per 10 seconds) based on API Key provided in each http call.
    * On exceeding the limit, api key must be suspended for next 5 minutes.
    * Api key can have different rate limit set, in this case from configuration, and if not present there must be a global rate limit applied.
2.  Search hotels by CityId
3.  Provide optional sorting of the result by Price (both ASC and DESC order).
Note: Please don’t use any external library or key-value store for RateLimit. You need to create a InMemory Implementation for RateLimit.

## Installing and running

This example was written in Python 3.5.2. Steps to install:

* Clone repository.
* Get into the cloned repo: `cd ratelimitpy`
* Create a virtual environment: `pyvenv-3.5 env` 
* Activate it: `. ./env/bin/activate`
* Install: `pip install .`
* Run: `FLASK_APP=ratelimitpy flask run`
* Hit with requests: `curl -H 'Authorization: Bearer potato' 'http://127.0.0.1:5000/hotels?city=Bangkok&asc=false'`
* Test with: `python setup.py test`

## Assumptions made

Here is a list of assumptions I've made while doing this assignment:

* The assignment talks about city id but I only found city name in the csv, so the search is by city name.
* The token bucket allows bursts of the number of requests you say per second. So if you say one request per 2 seconds, it allows only one request as a burst.
* When you're banned you have to wait the ban time and you're not penalized for trying again.
* The configuration for rate limit is for all endpoints.
* Python supports threads and it is common in production configurations to use them. It is true that only one thread runs at a time in python, but it can stop in the middle of something critical, that's why you will find locks in two critical areas of shared data.
* And for sure the quesiton of why python? It is easy to prototype functionality.
