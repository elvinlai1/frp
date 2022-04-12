# Generated by Django 4.0.1 on 2022-04-02 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClockList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('employee', models.CharField(max_length=30)),
                ('department', models.CharField(max_length=30)),
                ('in_time', models.CharField(max_length=30)),
                ('out_time', models.CharField(max_length=30)),
                ('hours', models.CharField(max_length=30)),
                ('work_time', models.CharField(max_length=30)),
                ('deduction', models.IntegerField()),
                ('notes', models.TextField()),
            ],
            options={
                'verbose_name': 'work',
                'verbose_name_plural': 'work',
                'db_table': 'race_work',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('department', models.CharField(max_length=30)),
                ('wage_per_hour', models.IntegerField()),
                ('face_encodings', models.TextField()),
                ('create_time', models.TextField()),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'user',
                'db_table': 'race_user',
            },
        ),
    ]