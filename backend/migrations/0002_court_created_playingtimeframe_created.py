# Generated by Django 4.1 on 2022-08-28 13:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='court',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 28, 13, 7, 19, 950092)),
        ),
        migrations.AddField(
            model_name='playingtimeframe',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 28, 13, 7, 19, 950289)),
        ),
    ]