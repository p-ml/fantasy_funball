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


if __name__ == "__main__":
    update_results(gameweek_no=1)
