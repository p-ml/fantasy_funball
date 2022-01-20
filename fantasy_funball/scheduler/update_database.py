import logging
import os

from fantasy_funball.logic.check_choices import (
    check_choices_if_deadline_day,
    check_teams_and_lineups,
)
from fantasy_funball.logic.determine_gameweek import determine_gameweek_no
from fantasy_funball.logic.update_fixtures import update_fixtures
from fantasy_funball.logic.update_results import update_results
from fantasy_funball.logic.update_standings import update_standings
from fantasy_funball.scheduler.update_players import update_players

logger = logging.getLogger("papertrail")


if __name__ == "__main__":
    # Run at midnight every day by Heroku Job Scheduler

    # Check if game is paused
    game_paused = os.environ.get("GAME_PAUSED")
    update_players()
    gameweek_no = determine_gameweek_no()

    logger.info(f"Game paused: {game_paused}")
    logger.info(f"Gameweek no: {gameweek_no}")

    if gameweek_no > 0 and not game_paused:
        check_choices_if_deadline_day(gameweek_no=gameweek_no)
        update_results(gameweek_no=gameweek_no)
        check_teams_and_lineups(gameweek_no=gameweek_no)
        update_standings(gameweek_no=gameweek_no)
        update_fixtures(gameweek_no=gameweek_no)

    else:
        print("Season has not started yet")
