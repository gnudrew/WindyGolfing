import pandas as pd

from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import WindGeneratorParameters, WindSpacetime
from .serializers import WindGeneratorParametersSerializer, WindSpacetimeSerializer
from .generators import OscillatoryGenerator, LorenzGenerator
from .wranglers import BlobWrangler

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

class WindSpacetimeViewSet(ModelViewSet):
    queryset = WindSpacetime.objects.all()
    serializer_class = WindSpacetimeSerializer
    
    def create(self, request, *args, **kwargs):
        # check existence
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            vdata = serializer.validated_data
            qs = self.get_queryset().filter(**vdata)
            if qs.count() != 0:
                print("This parameter set already exists.")
                return Response("This parameter set already exists.", status=409)

        # generate wind trajectory
        duration = vdata['duration']
        timestep = vdata['timestep']
        o = vdata['generator_parameters'] # Foreign Key
        if o.is_oscillatory:
            params = {
                'base_speed': o.base_speed,
                'amplitude': o.amplitude,
                'frequency': o.frequency,
                'phase_shift': o.phase_shift,
                'dt': timestep,
            }
            G = OscillatoryGenerator(params=params)
        elif o.is_lorenz:
            params = {
                'base_speed': o.base_speed, # m/s
                'rho': o.rho,
                'sigma': o.sigma,
                'beta': o.beta,
                'dt': timestep, # s
            }
            G = LorenzGenerator(params=params)

        arr_wind_speeds = G.gen(duration)
        df_wind_speeds = pd.DataFrame(arr_wind_speeds, columns=['x','y','z'])
        
        # store data (blob and obj)
        B = BlobWrangler()
        B.write_blob(df_wind_speeds, WindSpacetime, vdata)

        return Response("Created.")

    def destroy(self, request, *args, **kwargs):
        # destory blob

        return super().destroy(request, *args, **kwargs)