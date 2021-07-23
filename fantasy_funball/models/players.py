from django.db import models

from fantasy_funball.models.teams import Team


class Player(models.Model):
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
