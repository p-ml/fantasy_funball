import django

django.setup()

from fantasy_funball.scripts.setup_choices import setup_choices
from fantasy_funball.scripts.setup_fixtures import setup_fixtures
from fantasy_funball.scripts.setup_players import setup_players
from fantasy_funball.scripts.setup_results import setup_results
from fantasy_funball.scripts.setup_users import setup_users

if __name__ == "__main__":
    setup_users()
    setup_players()
    setup_fixtures()
    setup_choices()
    setup_results()
