from enum import auto
from django.db import models

class Timestamps(models.Model):
    employee_number = models.IntegerField()
    timestamp = models.CharField(max_length=30)
    status = models.CharField(max_length=3)

    class Meta(object):
        # Define table name
        db_table = 'timestamps'
    

