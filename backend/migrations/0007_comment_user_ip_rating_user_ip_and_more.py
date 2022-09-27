# Generated by Django 4.1 on 2022-09-27 15:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_address_street_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user_ip',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='rating',
            name='user_ip',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='comment',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]