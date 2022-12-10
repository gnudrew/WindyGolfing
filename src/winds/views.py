from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import WindGeneratorParameters
from .serializers import WindGeneratorParametersSerializer

class WindGeneratorParametersViewSet(ModelViewSet):
    queryset = WindGeneratorParameters.objects.all()
    serializer_class = WindGeneratorParametersSerializer

    def create(self, request, *args, **kwargs):
        # check existence
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            qs = self.get_queryset().filter(**serializer.validated_data)
            if qs.count() != 0:
                print("This parameter set already exists.")
                return Response("This parameter set already exists.", status=409)

        return super().create(request, *args, **kwargs)