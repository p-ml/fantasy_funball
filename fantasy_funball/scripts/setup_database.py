import os

import django

# These have to be set before any models are imported ¯\_(ツ)_/¯
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fantasy_funball.settings")
django.setup()

from fantasy_funball.scripts.setup_fixtures import setup_fixtures
from fantasy_funball.scripts.setup_users import setup_users

if __name__ == "__main__":
    setup_users()
    setup_fixtures()
