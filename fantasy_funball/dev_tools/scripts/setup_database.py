from fantasy_funball.dev_tools.scripts import (
    setup_choices,
    setup_fixtures,
    setup_gamedays,
    setup_gameweeks,
    setup_players,
    setup_results,
    setup_teams,
    setup_users,
)
from fantasy_funball.logic.random_generator import generate_steve_choices

if __name__ == "__main__":
    """Completely wipes the db and sets it up again from scratch"""
    setup_gameweeks()
    setup_gamedays()
    setup_teams()
    setup_players()
    setup_users()
    setup_fixtures()
    setup_choices()
    setup_results()
    generate_steve_choices()
