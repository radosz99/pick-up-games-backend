from rest_framework import serializers
from .models import Court, Address, CourtDetails, PlayingTimeFrame
from .services.court_service import convert_unix_timestamp_to_date
import logging


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('country', 'city', 'street_name', 'postal_code', 'latitude', 'longitude', 'street_number')


class CourtDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtDetails
        fields = ('courts_number', 'hoops_number', 'lightning', 'surface', 'type', 'public', 'rim_type')


class CourtSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    details = CourtDetailsSerializer()

    class Meta:
        model = Court
        fields = ('id', 'name', 'address', 'details', 'created', 'expected_players_number', 'actual_players_number')

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
        start = validated_data.pop('start')
        end = validated_data.pop('end')
        start = convert_unix_timestamp_to_date(start)
        end = convert_unix_timestamp_to_date(end)
        logging.debug(start)
        logging.debug(end)
        court = validated_data.pop('court')
        logging.debug(validated_data)
        timeframe_instance = PlayingTimeFrame.objects.create(start=start, end=end, court_id=court.id, **validated_data)
        return timeframe_instance
