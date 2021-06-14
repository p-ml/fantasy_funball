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
`fantasy_funball` directory and `docker-compose up`. Voila MongoDB instance up and 
running. You can now mess around with your local MongoDB instance. If you want to
reset & add test data, run `fantasy_funball/scripts/setup_database.py`

Alternatively, you could install MongoDB locally, and point the env. var `MONGO_DB_URL`
at your local MongoDB.

### Environment Variables
Environment variables needed are listed in `.env.sample`. Make a copy called `.env`.
You'll need to add a path to your chrome driver for Selenium, and MongoDB URL.
If running PyCharm, get the `EnvFile` plugin, which allows you to attach an `.env` file to any run
configuration.

## Notes
Project has been set up with a default Django template, idea being that eventually 
this repo will be hosted somewhere (in the :cloud:) so need to be able to hit that.
`core/` contains generic django files, whereas `fantasy_funball/` contains the bulk
of the application code.

## Basic Idea / Structure
![Potential Structure](docs/fantasy_funball_structure.png)