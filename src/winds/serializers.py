from rest_framework import serializers 

from .models import WindGenParams, WindSpacetime

class WindGenParamsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WindGenParams
        fields = '__all__'

class WindSpacetimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WindSpacetime
        exclude = [
            'blob_filename'
        ]