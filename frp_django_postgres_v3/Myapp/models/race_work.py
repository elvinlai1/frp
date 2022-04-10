from django.db import models


class ClockList(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    in_time = models.CharField(max_length=30)
    out_time = models.CharField(max_length=30)
    hours = models.CharField(max_length=30)
    work_time = models.CharField(max_length=30)
    deduction = models.IntegerField()
    notes = models.TextField()

    class Meta(object):
        # Define table name
        db_table = 'race_work'
        # Database table name set to 'work'
        verbose_name = 'work'
        # Set 'work' plural to be 'work'
        verbose_name_plural = verbose_name
