# Fantasy Funball 2: Electric Boogaloo

Fantasy Funball Backend API. Accompanied by a Streamlit app to act as a front end.


[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/p-ml/fantasy_funball_streamlit/fantasy_funball.py)
![Testing Workflow](https://github.com/p-ml/fantasy_funball/actions/workflows/testing_workflow.yml/badge.svg)

## Project Structure
All of the _fantasy_funball_ logic is stored within the `fantasy_funball` app.
- `dev_tools/`: Contains various admin/setup scripts, **NOT** to be used in production.
- `fpl_interface/`: Interacts with the Fantasy Premier League API.
- `logic/`: Bulk of the application's day-to-day running logic.
- `migrations/`: Django migrations.
- `models/`: Django models.
- `scheduler/`: The `update_database.py` script is what is run each night at 00:00 UTC by Heroku Scheduler.
- `tests/`: Various unit tests.
- `views/`: Django Rest Framework influenced views as an entry-point for the requests to the app.
- `urls.py`: Each of the app's endpoints.


## Local Deployment
The app is fully dockerised - With `docker-compose` installed locally, simply navigating to the `fantasy-funball`
folder and running `docker-compose up` should have the app running locally on your machine.

This consists of two containers: `app` which runs the Django server, and `postgres` which hosts the PostgreSQL database.
All required environment variables can be found in `.env.docker`

Alternatively, you can run the app without docker via the usual Django `manage.py runserver` commands. Note that you'll need
the environment variables listed in `.env.sample`.

## Hosted Deployment
The app is hosted on Heroku, where a GitHub Action has been set up to automatically deploy to Heroku on every push to `master`.
A Heroku PostgreSQL database is used, along with Papertrail and Sentry for logging/monitoring.


## Dependency Management, Testing & Linting
Poetry is used for dependency management, but a `requirements.txt` file is still required by Heroku. This can be generated
via the `poetry export --without-hashes --output requirements.txt` command.

`pytest` is used for testing. Functional tests are run against a Dockerised version of the app. A GitHub Action has been set up
to automatically run the unit and functional tests on every push.

A combination of `black`, `isort` and `flake8` are used for linting. These are enforced by `pre-commit` hooks, which should be installed 
locally with `pre-commit install`. The config for the linters can be found in `tox.ini` and `pyproject.toml`.

## Todo
- Bulk out tests (both unit and functional)
