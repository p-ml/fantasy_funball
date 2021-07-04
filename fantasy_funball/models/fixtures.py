from django.db import models


class Gameweek(models.Model):
    deadline = models.DateTimeField()


class Gameday(models.Model):
    date = models.DateTimeField()
    gameweek = models.ForeignKey(Gameweek, on_delete=models.CASCADE)


class Result(models.Model):
    home_team = models.CharField(max_length=20)
    home_score = models.IntegerField()
    away_team = models.CharField(max_length=20)
    away_score = models.IntegerField()
    gameday = models.ForeignKey(Gameday, on_delete=models.DO_NOTHING)


class Fixture(models.Model):
    home_team = models.CharField(max_length=20)
    away_team = models.CharField(max_length=20)
    kickoff = models.CharField(max_length=20)
    gameday = models.ForeignKey(Gameday, on_delete=models.DO_NOTHING)
