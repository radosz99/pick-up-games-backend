import logging
from datetime import datetime, timezone
from rest_framework import serializers
from django.db.models import Avg

from .models import Court, Address, CourtDetails, PlayingTimeFrame, CourtImage, Rating, Comment
from .services.court_service import convert_unix_timestamp_to_date, calculate_distance_between_two_coordinates


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('country', 'city', 'street_name', 'postal_code', 'latitude', 'longitude', 'street_number')


class CourtDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtDetails
        fields = ('courts_number', 'hoops_number', 'lightning', 'surface', 'type', 'public', 'rim_type')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtImage
        fields = ('id', 'court', 'image')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'court', 'stars', 'user_ip')

    def create(self, validated_data):
        logging.debug(f"Creating rating from - {validated_data}")
        stars = validated_data.pop('stars')
        court = validated_data.pop('court')
        if stars > 5.0:
            raise serializers.ValidationError("Rating can not exceed maximum which is 5.0")
        court_instance = Rating.objects.create(stars=stars, court_id=court.id, **validated_data)
        return court_instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'court', 'content', 'user_ip')

    def create(self, validated_data):
        logging.debug(f"Creating comment from - {validated_data}")
        content = validated_data.pop('content')
        court = validated_data.pop('court')
        court_instance = Comment.objects.create(content=content, court_id=court.id, **validated_data)
        return court_instance


class CourtSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    details = CourtDetailsSerializer()
    distance = serializers.SerializerMethodField('calculate_distance')
    rating = serializers.SerializerMethodField('calculate_average_rating')
    ratings_number = serializers.SerializerMethodField('count_ratings')
    expected_players_number = serializers.SerializerMethodField('calculate_expected_players_number')

    def calculate_average_rating(self, court):
        rating = court.ratings.aggregate(Avg('stars'))
        rating = 0 if rating['stars__avg'] is None else rating['stars__avg']
        logging.debug(f"Rating {rating} for court with id = {court.id}")
        return rating

    def count_ratings(self, court):
        count = court.ratings.all().count()
        logging.debug(f"{count} ratings for court with id = {court.id}")
        return count

    def calculate_expected_players_number(self, court):
        expected_players_number = 0
        now = datetime.now(timezone.utc)
        active_timeframes = PlayingTimeFrame.objects.filter(court_id=court.id).filter(finished=False)
        logging.debug(f"Active timeframes for court_id = {court.id} number is {len(active_timeframes)}")
        for timeframe in active_timeframes:
            if timeframe.end >= now >= timeframe.start:
                expected_players_number += 1
        logging.debug(f"Current expected players number for court_id = {court.id} is {expected_players_number}")
        return expected_players_number

    def calculate_distance(self, court):
        latitude, longitude = self.context.get('lat'), self.context.get('lon')
        if latitude is None or longitude is None:
            logging.debug('Latitude and longitude are not set, returning -1 as distance')
            return -1
        else:
            return calculate_distance_between_two_coordinates(latitude,
                                                              longitude,
                                                              court.address.latitude,
                                                              court.address.longitude)

    class Meta:
        model = Court
        fields = ('id', 'name', 'address', 'details', 'created', 'expected_players_number',
                  'actual_players_number', 'distance', 'rating', 'ratings_number')

    def create(self, validated_data):
        address = validated_data.pop('address', None)
        details = validated_data.pop('details', None)
        address_instance = Address.objects.create(**address)
        details_instance = CourtDetails.objects.create(**details)
        court_instance = Court.objects.create(address=address_instance, details=details_instance, **validated_data)
        return court_instance


class TimeFrameSerializer(serializers.ModelSerializer):
    start = serializers.CharField(max_length=10, min_length=10)
    end = serializers.CharField(max_length=10, min_length=10)

    class Meta:
        model = PlayingTimeFrame
        fields = ('id', 'player_nick', 'court', 'start', 'end')

    def create(self, validated_data):
        logging.debug(f"Creating timeframe from - {validated_data}")
        start = validated_data.pop('start')
        end = validated_data.pop('end')
        start = convert_unix_timestamp_to_date(start)
        end = convert_unix_timestamp_to_date(end)
        court = validated_data.pop('court')
        timeframe_instance = PlayingTimeFrame.objects.create(start=start, end=end, court_id=court.id, **validated_data)
        return timeframe_instance
