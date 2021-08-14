import django

django.setup()

from fantasy_funball.models import Funballer


def reset_standings():
    """Reset all funballer points back to zero"""
    all_funballers = Funballer.objects.all()

    for funballer in all_funballers:
        funballer.player_points = 0
        funballer.team_points = 0
        funballer.points = 0
        funballer.save()


if __name__ == "__main__":
    reset_standings()
