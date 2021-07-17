from django.db import models

from fantasy_funball.models import Gameweek
from fantasy_funball.models.players import Player
from fantasy_funball.models.teams import Team


class Funballer(models.Model):
    first_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    player_points = models.IntegerField()
    team_points = models.IntegerField()
    points = models.IntegerField()


class Choices(models.Model):
    funballer = models.ForeignKey(Funballer, on_delete=models.DO_NOTHING)
    gameweek = models.ForeignKey(Gameweek, on_delete=models.DO_NOTHING)

    team_choice = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    player_choice = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
