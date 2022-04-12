from django.db import models

class Employees(models.Model):
    employee_number = models.IntegerField(primary_key=True)
    employee_name = models.TextField()
    department = models.CharField(max_length=30)

    class Meta(object):
        # Define table name
        db_table = 'employees'
    
