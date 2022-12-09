from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from .models import WindGeneratorParameters
from .serializers import WindGeneratorParametersSerializer

class WindGeneratorParametersViewSet(ModelViewSet):
    queryset = WindGeneratorParameters.objects.all()
    serializer_class = WindGeneratorParametersSerializer
