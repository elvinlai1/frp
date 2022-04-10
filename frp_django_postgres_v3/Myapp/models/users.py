from django.db import models

class Users(models.Model):
    emp_num = models.IntegerField(primary_key=True)
    emp_name = models.CharField(max_length=30)
    department = models.CharField(max_length=30)

    class Meta(object):
        # Define table name
        db_table = 'users'
        verbose_name = 'Users'
