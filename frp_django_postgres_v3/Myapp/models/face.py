from django.db import models

class Face(models.Model):
    emp_num = models.IntegerField(primary_key=True)
    emp_name = models.TextField()
    emp_encodings = models.BinaryField(null=True)

    class Meta(object):
        # Define table name
        db_table = 'face'
