from django.db import models


class Date(models.Model):
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    day = models.CharField(max_length=2)
    hour = models.CharField(max_length=2)
    minute = models.CharField(max_length=2)
