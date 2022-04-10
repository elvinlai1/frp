from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    wage_per_hour = models.IntegerField()
    face_encodings = models.TextField()
    create_time = models.TextField()

    def __str__(self):
        return self.first_name

    class Meta(object):
        # define table name
        db_table = 'race_user'
        # Database table name set to 'user'
        verbose_name = 'user'
        # Set 'user' plural to be 'user'）
        verbose_name_plural = verbose_name
