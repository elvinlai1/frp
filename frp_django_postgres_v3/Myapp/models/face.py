from django.db import models


class Face(models.Model):
    emp_num = models.AutoField(primary_key=True)
    emp_name = models.CharField(max_length=None)
    emp_encodings = models.BinaryField(null=True)

    class Meta(object):
        # Define table name
        db_table = 'face'
