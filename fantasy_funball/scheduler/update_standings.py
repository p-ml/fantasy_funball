from fantasy_funball.logic.determine_gameweek import determine_gameweek_no
from fantasy_funball.logic.update_standings import update_standings

if __name__ == "__main__":
    # Run at midnight every day by Heroku Job Scheduler
    gameweek_no = determine_gameweek_no()
    update_standings(gameweek_no=gameweek_no)
