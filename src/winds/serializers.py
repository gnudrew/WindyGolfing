from rest_framework import serializers 

from .models import WindGeneratorParameters

class WindGeneratorParametersSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = WindGeneratorParameters
        fields = '__all__'