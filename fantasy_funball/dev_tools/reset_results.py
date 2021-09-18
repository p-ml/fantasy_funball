import django

django.setup()

from fantasy_funball.models import Assists, Goals, Result


def reset_goals():
    """Delete all goals from the db"""
    all_goals = Goals.objects.all()

    for goal in all_goals:
        goal.delete()


def reset_assists():
    """Delete all assists from the db"""
    all_assists = Assists.objects.all()

    for assist in all_assists:
        assist.delete()


def reset_results():
    """Delete all results from the db"""
    all_results = Result.objects.all()

    for result in all_results:
        result.delete()


if __name__ == "__main__":
    reset_goals()
    reset_assists()
    reset_results()
