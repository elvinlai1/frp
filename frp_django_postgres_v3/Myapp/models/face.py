from django.db import models

class Face(models.Model):
    employee_number = models.IntegerField(primary_key=True)
    encodings = models.BinaryField(null=True)

    class Meta(object):
        # Define table name
        db_table = 'face'
