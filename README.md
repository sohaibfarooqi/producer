# Producer
[![Build Status](https://travis-ci.org/sohaibfarooqi/producer.svg?branch=master)](https://travis-ci.org/sohaibfarooqi/producer)   [![Coverage Status](https://coveralls.io/repos/github/sohaibfarooqi/producer/badge.svg?branch=master)](https://coveralls.io/github/sohaibfarooqi/producer?branch=master)  [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/sohaibfarooqi/producer/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/sohaibfarooqi/producer/?branch=master)

This app implements a producer component of classic [Producer-Consumer Architecture](https://en.wikipedia.org/wiki/Producer%E2%80%93consumer_problem). It exposes a web API which accepts CSV files. CSV files are passed to a celery
task. This task reads all the data from file based on specified format and push everything to attached broker.
For this application the choice of broker is limited to the ones which support named queues creation.

### Installation and Running
The following steps will get you a copy of app(single instance) on you local system:

  - `git clone https://github.com/sohaibfarooqi/producer.git`
  - `cd producer`
  - `virtualenv -p python3 .venv`
  - `source .venv/bin/activate`
  - `pip install -r requirements/dev.txt`
  - `set environemnt variable CELERY_BROKER_URL=amqp://myuser:mypassword@localhost:5672/myvhost`
  - `export FLASK_APP=producer`

Run the following two commands in two seperate shells

  - `flask run`
  - `celery -A producer worker -l info`

At this point the app is ready to accept new files. Use the following script to test:

```
import requests
files = {'file': open('test.csv', 'r')}
requests.post('http://localhost:5000/upload', files=files)
```

**NOTE** By default the producer will send messages to `test` queue and expect consumer to
be a celery task named `consumer`.

### Pre-commit hooks
  - Run `pre-commit install` to enable the hook into your git repo. The hook will run automatically for each commit.
  - Run `git commit -m "Your message" -n` to skip the hook if you need.
