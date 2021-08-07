import django

django.setup()

from fantasy_funball.scripts import (
    setup_choices,
    setup_fixtures,
    setup_gamedays,
    setup_gameweeks,
    setup_players,
    setup_results,
    setup_teams,
    setup_users,
)

if __name__ == "__main__":
    setup_gameweeks()
    setup_gamedays()
    setup_teams()
    setup_players()
    setup_users()
    setup_fixtures()
    setup_choices()
    setup_results()
