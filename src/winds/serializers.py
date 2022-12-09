from rest_framework.serializers import HyperlinkedModelSerializer

from .models import WindGeneratorParameters

class WindGeneratorParametersSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = WindGeneratorParameters
        fields = '__all__'