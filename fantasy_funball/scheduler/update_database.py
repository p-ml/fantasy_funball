import logging
import os
from datetime import date

from fantasy_funball.logic import (
    check_choices_if_deadline_day,
    check_teams_and_lineups,
    determine_gameweek_no,
    update_fixtures,
    update_players,
    update_results,
    update_standings,
)

logger = logging.getLogger("papertrail")

if __name__ == "__main__":
    # Run at midnight every day by Heroku Job Scheduler

    # Check if game is paused
    game_resume = os.environ.get("GAME_RESUME")
    update_players()
    gameweek_no = determine_gameweek_no()

    logger.info(
        f"Game paused: {game_resume}\n"
        f"Todays date: {date.today()}\n"
        f"Gameweek no: {gameweek_no}\n"
    )
    logger.info()

    if gameweek_no > 0 and game_resume:
        check_choices_if_deadline_day(gameweek_no=gameweek_no)
        update_results(gameweek_no=gameweek_no)
        check_teams_and_lineups(gameweek_no=gameweek_no)
        update_standings(gameweek_no=gameweek_no)
        update_fixtures(gameweek_no=gameweek_no)

    else:
        logger.info("Season has not started yet\n")
