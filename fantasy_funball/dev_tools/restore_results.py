from fantasy_funball.logic.determine_gameweek import determine_gameweek_no
from fantasy_funball.logic.update_results import update_results

if __name__ == "__main__":
    """Restores results for all gameweeks"""
    gameweek_no = determine_gameweek_no()
    for i in range(1, gameweek_no):
        update_results(gameweek_no=i)
