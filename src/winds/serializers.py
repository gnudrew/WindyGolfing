from rest_framework import serializers 

from .models import WindGenParams, WindSpacetime

class WindGenParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindGenParams
        fields = '__all__'

class WindSpacetimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindSpacetime
        exclude = [
            'blob_filename'
        ]