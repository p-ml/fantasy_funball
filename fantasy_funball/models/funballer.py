from djongo import models


class Funballer(models.Model):
    first_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    points = models.IntegerField()
