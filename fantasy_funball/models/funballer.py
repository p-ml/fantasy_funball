from django.db import models


class Funballer(models.Model):
    first_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20, null=True, blank=True)
    player_points = models.IntegerField()
    team_points = models.IntegerField()
    points = models.IntegerField()
    pin = models.CharField(max_length=4, unique=True)
