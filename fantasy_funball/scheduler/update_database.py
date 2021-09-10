from fantasy_funball.helpers.date import determine_if_transfer_window
from fantasy_funball.logic.check_choices import check_choices, check_lineups
from fantasy_funball.logic.determine_gameweek import determine_gameweek_no
from fantasy_funball.logic.update_results import update_results
from fantasy_funball.logic.update_standings import update_standings
from fantasy_funball.scheduler.update_players import update_players

if __name__ == "__main__":
    # Run at midnight every day by Heroku Job Scheduler
    gameweek_no = determine_gameweek_no()
    if gameweek_no > 0:
        check_choices(gameweek_no=gameweek_no)
        update_results(gameweek_no=gameweek_no)
        check_lineups(gameweek_no=gameweek_no)
        update_standings(gameweek_no=gameweek_no)

    else:
        print("Season has not started yet")

    is_transfer_window = determine_if_transfer_window()
    if is_transfer_window:
        update_players()
