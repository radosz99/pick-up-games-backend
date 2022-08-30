from rest_framework import serializers
from .models import Court, Address, CourtDetails


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('country', 'city', 'street_name', 'postal_code', 'latitude', 'longitude', 'street_number')


class CourtDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtDetails
        fields = ('courts_number', 'hoops_number', 'lightning', 'surface')


class CourtSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    details = CourtDetailsSerializer()

    class Meta:
        model = Court
        fields = ('id', 'name', 'address', 'details', 'created')

    def create(self, validated_data):
        address = validated_data.pop('address', None)
        details = validated_data.pop('details', None)
        address_instance = Address.objects.create(**address)
        details_instance = CourtDetails.objects.create(**details)
        court_instance = Court.objects.create(address=address_instance, details=details_instance, **validated_data)
        return court_instance


