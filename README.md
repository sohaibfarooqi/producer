## Producer
This app implements a producer component of classic [Producer-Consumer Architecture](https://en.wikipedia.org/wiki/Producer%E2%80%93consumer_problem). It exposes a web API which accepts CSV files. CSV files are passed to a celery
task. This task reads all the data from file based on specified format and push everything to attached broker.
For this application the choice of broker is limited to the ones which support named queues creation.

in the database.
## Pre-commit hooks
  - Run `pre-commit install` to enable the hook into your git repo. The hook will run automatically for each commit.
  - Run `git commit -m "Your message" -n` to skip the hook if you need.
