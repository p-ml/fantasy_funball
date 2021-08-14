import django

django.setup()

from fantasy_funball.models import Result


def reset_results():
    """Delete all results from the db"""
    all_results = Result.objects.all()

    for result in all_results:
        result.delete()


if __name__ == "__main__":
    reset_results()
