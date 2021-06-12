import django

django.setup()

from fantasy_funball.scripts.setup_fixtures import setup_fixtures
from fantasy_funball.scripts.setup_users import setup_users

if __name__ == "__main__":
    setup_users()
    setup_fixtures()
