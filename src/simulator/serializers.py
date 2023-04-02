from rest_framework.serializers import ModelSerializer

from .models import SimExperiment

class SimExperimentSerializer(ModelSerializer):
    class Meta:
        model = SimExperiment
        exclude = ['simtrials']