from django.db import models


class Funballer(models.Model):
    first_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    points = models.IntegerField()


class Choices(models.Model):
    funballer_id = models.ForeignKey(Funballer, on_delete=models.CASCADE)
    choices = models.JSONField()
