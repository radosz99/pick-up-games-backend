# Generated by Django 4.1 on 2022-08-28 13:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_court_created_playingtimeframe_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 28, 13, 8, 46, 525708)),
        ),
        migrations.AlterField(
            model_name='playingtimeframe',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 28, 13, 8, 46, 525918, tzinfo=datetime.timezone.utc)),
        ),
    ]