import pandas as pd

from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import WindGenParams, WindSpacetime
from .serializers import WindGenParamsSerializer, WindSpacetimeSerializer
from .generators import OscillatoryGenerator, LorenzGenerator

from commons.wranglers import BlobWrangler

class WindGenParamsViewSet(ModelViewSet):
    queryset = WindGenParams.objects.all()
    serializer_class = WindGenParamsSerializer

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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            vdata = serializer.validated_data
            qs = self.get_queryset().filter(**vdata)
            if qs.count() != 0:
                print("This parameter set already exists.")
                return Response("This parameter set already exists.", status=409)

            # generate wind trajectory
            duration = vdata['duration']
            timestep = vdata['timestep']
            o = vdata['generator_params'] # ForeignKey --> serializer should convert str to obj
            if o.is_oscillatory:
                params = {
                    'base_velocity': o.base_velocity,
                    'amplitude': o.amplitude,
                    'frequency': o.frequency,
                    'phase_offset': o.phase_offset,
                    'dt': timestep,
                }
                G = OscillatoryGenerator(params=params)
            elif o.is_lorenz:
                params = {
                    'base_velocity': o.base_velocity, # m/s
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
        else:
            return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # destory blob
        o = self.get_object()
        BlobWrangler().delete_blob(o)

        # destroy obj as usual...
        return super().destroy(request, *args, **kwargs)