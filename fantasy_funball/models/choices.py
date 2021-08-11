from django.db import models

from fantasy_funball.models import Funballer, Gameweek, Player, Team


class Choices(models.Model):
    funballer = models.ForeignKey(Funballer, on_delete=models.DO_NOTHING)
    gameweek = models.ForeignKey(Gameweek, on_delete=models.DO_NOTHING)

    team_choice = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    player_choice = models.ForeignKey(Player, on_delete=models.DO_NOTHING)

    team_has_been_processed = models.BooleanField(default=False)
    player_has_been_processed = models.BooleanField(default=False)
