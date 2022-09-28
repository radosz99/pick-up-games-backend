import django
from django.db import models


class Address(models.Model):
    country = models.CharField(max_length=50)  # consider Enum for countries
    city = models.CharField(max_length=30)
    street_name = models.CharField(max_length=30, blank=True)
    postal_code = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()
    street_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return str(self.__dict__)


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

    class CourtType(models.TextChoices):
        INDOOR = 'Indoor'
        OUTDOOR = 'Outdoor'

    class RimType(models.TextChoices):
        HIGHER = 'Higher'
        LOWER = 'Lower'
        NORMAL = 'Normal'
        VARIOUS = 'Various'

    courts_number = models.IntegerField()
    hoops_number = models.IntegerField()
    lightning = models.BooleanField(default=False)
    surface = models.CharField(choices=SurfaceType.choices, default=SurfaceType.OTHER, max_length=20)
    type = models.CharField(choices=CourtType.choices, default=CourtType.OUTDOOR, max_length=10)
    public = models.BooleanField(default=True)
    rim_type = models.CharField(choices=RimType.choices, default=RimType.NORMAL, max_length=10)

    def __str__(self):
        return str(self.__dict__)


class Court(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True, related_name='court')
    details = models.ForeignKey(CourtDetails, on_delete=models.CASCADE, null=True, blank=True, related_name='court')
    created = models.DateTimeField(default=django.utils.timezone.now)
    actual_players_number = models.IntegerField(default=0)

    def __str__(self):
        return str(self.__dict__)


class PlayingTimeFrame(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    player_nick = models.CharField(max_length=20)
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='timeframes')
    created = models.DateTimeField(default=django.utils.timezone.now)
    finished = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return str(self.__dict__)


class Comment(models.Model):
    content = models.TextField()
    creation_date = models.DateTimeField(default=django.utils.timezone.now)
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='comments')
    user_ip = models.CharField(max_length=20, blank=True)


class Rating(models.Model):
    stars = models.FloatField()
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='ratings')
    creation_date = models.DateTimeField(default=django.utils.timezone.now)
    user_ip = models.CharField(max_length=20, blank=True)


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class CourtImage(models.Model):
    image = models.ImageField(upload_to=upload_to)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)




