from .setup_choices import setup_choices
from .setup_fixtures import setup_fixtures
from .setup_gamedays import setup_gamedays
from .setup_gameweeks import setup_gameweeks
from .setup_players import setup_players
from .setup_results import setup_results
from .setup_teams import setup_teams
from .setup_users import setup_users

__all__ = [
    setup_users,
    setup_gameweeks,
    setup_gamedays,
    setup_players,
    setup_teams,
    setup_results,
    setup_choices,
    setup_fixtures,
]
