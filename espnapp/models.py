from django.db import models
from django.db.models.fields.related import ManyToManyField


class Players(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    age = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Squads(models.Model):
    name = models.CharField(max_length=100)
    squad = ManyToManyField(Players)
    series = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name+'-'+self.series
