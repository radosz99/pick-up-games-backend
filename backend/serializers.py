from rest_framework import serializers
from .models import Court, Address, CourtDetails


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('country', 'city', 'street_name', 'postal_code', 'latitude', 'longitude', 'street_number')


class CourtDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourtDetails
        fields = ('courts_number', 'hoops_number', 'lightning', 'surface')


class CourtSerializer(serializers.HyperlinkedModelSerializer):
    address = AddressSerializer()
    details = CourtDetailsSerializer()

    class Meta:
        model = Court
        fields = ('id', 'name', 'address', 'details', 'created')




