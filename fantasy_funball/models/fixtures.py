from django.db import models

from fantasy_funball.models import Player, Team


class Gameweek(models.Model):
    deadline = models.DateTimeField()
    gameweek_no = models.IntegerField()


class Gameday(models.Model):
    date = models.DateTimeField()
    gameweek = models.ForeignKey(Gameweek, on_delete=models.CASCADE)


class Result(models.Model):
    home_team = models.ForeignKey(
        Team, on_delete=models.DO_NOTHING, related_name="result_home_team"
    )
    home_score = models.IntegerField()
    away_team = models.ForeignKey(
        Team, on_delete=models.DO_NOTHING, related_name="result_away_team"
    )
    away_score = models.IntegerField()
    gameday = models.ForeignKey(Gameday, on_delete=models.DO_NOTHING)

    scorers = models.ManyToManyField(Player, related_name="scorers")
    assists = models.ManyToManyField(Player, related_name="assists")


class Fixture(models.Model):
    home_team = models.ForeignKey(
        Team, on_delete=models.DO_NOTHING, related_name="fixture_home_team"
    )
    away_team = models.ForeignKey(
        Team, on_delete=models.DO_NOTHING, related_name="fixture_away_team"
    )
    kickoff = models.CharField(max_length=20)
    gameday = models.ForeignKey(Gameday, on_delete=models.DO_NOTHING)
