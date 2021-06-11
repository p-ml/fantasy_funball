import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fantasy_funball.settings")
django.setup()

from fantasy_funball.scripts.setup_users import setup_users

if __name__ == "__main__":
    setup_users()
