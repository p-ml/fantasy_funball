# Fantasy Funball 2: Electric Boogaloo

## Setup
### Python Environment
Consider using a virtual environment; navigate to `fantasy_funball` directory and:
```python -m venv <virtual env name>```

Once set up, install required packages using requirements.txt
`pip install -r requirements.txt`. Please add to this as you need more packages.

### Database Setup
To run database locally, use Docker :whale:. Install both 
[Docker](https://docs.docker.com/get-docker/) and 
[Docker Compose](https://docs.docker.com/compose/install/). Then navigate to 
`fantasy_funball` directory and `docker-compose up`. Voila Postgres instance up and 
running. You can now mess around with your local Postgres instance. If you want to
reset & add test data, run `fantasy_funball/scripts/setup_database.py`

Alternatively, you could install PostgreSQL locally, and fill out the environment
variables within `.env` to point at your local postgres db

### Environment Variables
Environment variables needed are listed in `.env.sample`. Make a copy called `.env`.
You'll need to add a path to your chrome driver for Selenium, and Postgres creds.
If running PyCharm, get the `EnvFile` plugin, which allows you to attach an `.env` file to any run
configuration.

## Notes
Project has been set up with a default Django template, idea being that eventually 
this repo will be hosted somewhere (in the :cloud:) so need to be able to hit that.
`core/` contains generic django files, whereas `fantasy_funball/` contains the bulk
of the application code.

## Basic Idea / Structure
![Potential Structure](docs/fantasy_funball_structure.png)

## Todo
- Logic to check results, update funballer points, determine standings
- Job scheduler to run every night
- Check if scraper works with fixtures in the future, rather than the past **(21/22 fixtures released 16th June, waiting for FPL website to be updated)**
- Basic front end of some sort
- Bulk out tests (both unit and functional)
