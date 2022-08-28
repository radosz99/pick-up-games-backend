import django
from django.db import models

from datetime import datetime


class Address(models.Model):
    country = models.CharField(max_length=50)  # consider Enum for countries
    city = models.CharField(max_length=30)
    street_name = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()
    street_number = models.CharField(max_length=20)


class CourtDetails(models.Model):
    class SurfaceType(models.TextChoices):
        CEMENT = 'Cement'
        CONCRETE = 'Concrete'
        DIRT = 'Dirt'
        GRASS = 'Grass'
        PLASTIC = 'Plastic'
        RUBBER = 'Rubber'
        WOOD = 'Wood'
        OTHER = 'Other'

    courts_number = models.IntegerField()
    hoops_number = models.IntegerField()
    lightning = models.BooleanField()
    surface = models.CharField(choices=SurfaceType.choices, default=SurfaceType.OTHER, max_length=20)


class Court(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    details = models.ForeignKey(CourtDetails, on_delete=models.CASCADE)
    created = models.DateTimeField(default=django.utils.timezone.now)


class PlayingTimeFrame(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    player_nick = models.CharField(max_length=20)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    created = models.DateTimeField(default=django.utils.timezone.now)


class Comment(models.Model):
    content = models.TextField()
    creation_date = models.DateTimeField()
    court = models.ForeignKey(Court, on_delete=models.CASCADE)


class Rating(models.Model):
    stars = models.FloatField()
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    creation_date = models.DateTimeField()


class CourtImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    court = models.ForeignKey(Court, on_delete=models.CASCADE)




