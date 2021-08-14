import django

from fantasy_funball.fpl_interface.interface import FPLInterface

django.setup()

from fantasy_funball.models import Result


def update_results(gameweek_no: int):
    """Retrieves results from FPL API and saves to db"""

    fpl_interface = FPLInterface()
    gameweek_results = fpl_interface.retrieve_gameweek_results(
        gameweek_no=gameweek_no,
    )

    gameweek_scorers = fpl_interface.retrieve_weekly_scorers(
        gameweek_no=gameweek_no,
    )
    gameweek_assists = fpl_interface.retrieve_weekly_assists(
        gameweek_no=gameweek_no,
    )

    for result in gameweek_results:
        result_obj = Result(
            home_team=result["home_team"],
            home_score=result["home_score"],
            away_team=result["away_team"],
            away_score=result["away_score"],
            gameday_id=result["gameday"],
        )

        # Only save if result doesn't already exist - may be a better solution
        try:
            Result.objects.get(
                home_team=result["home_team"],
                home_score=result["home_score"],
                away_team=result["away_team"],
                away_score=result["away_score"],
                gameday_id=result["gameday"],
            )

        except Result.DoesNotExist:
            result_obj.save()

            home_scorers = gameweek_scorers[result["home_team"].team_name]
            away_scorers = gameweek_scorers[result["away_team"].team_name]

            home_assists = gameweek_assists[result["home_team"].team_name]
            away_assists = gameweek_assists[result["away_team"].team_name]

            for scorer_id in home_scorers.union(away_scorers):
                result_obj.scorers.add(scorer_id)

            for assist_id in home_assists.union(away_assists):
                result_obj.assists.add(assist_id)


if __name__ == "__main__":
    update_results(gameweek_no=1)
