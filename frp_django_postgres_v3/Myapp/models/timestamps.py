from django.db import models

class Timestamps(models.Model):
    emp_num = models.IntegerField(primary_key=True)
    emp_timestamp = models.CharField(max_length=None)
    emp_status = models.CharField(max_length=3)

    class Meta(object):
        # Define table name
        db_table = 'timestamps'
        verbose_name = 'Timestamps'

