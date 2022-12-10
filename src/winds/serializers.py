from rest_framework import serializers 

from .models import WindGeneratorParameters, WindSpacetime

class WindGeneratorParametersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WindGeneratorParameters
        fields = '__all__'

class WindSpacetimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WindSpacetime
        fields = '__all__'