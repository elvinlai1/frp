# Generated by Django 4.0.1 on 2022-04-14 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0002_alter_timestamps_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='employee_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='timestamps',
            name='timestamp',
            field=models.CharField(max_length=30),
        ),
    ]
