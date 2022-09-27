from rest_framework import serializers
from .models import Court, Address, CourtDetails, PlayingTimeFrame, CourtImage, Rating
from .services.court_service import convert_unix_timestamp_to_date, calculate_distance_between_two_coordinates
import logging


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
        court_instance = Rating.objects.create(stars=stars, court_id=court.id, **validated_data)
        return court_instance


class CourtSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    details = CourtDetailsSerializer()
    distance = serializers.SerializerMethodField('calculate_distance')

    def calculate_distance(self, court):
        latitude, longitude = self.context.get('lat'), self.context.get('lon')
        if latitude is None or longitude is None:
            return -1
        else:
            return calculate_distance_between_two_coordinates(latitude,
                                                              longitude,
                                                              court.address.latitude,
                                                              court.address.longitude)

    class Meta:
        model = Court
        fields = ('id', 'name', 'address', 'details', 'created', 'expected_players_number', 'actual_players_number', 'distance')

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
