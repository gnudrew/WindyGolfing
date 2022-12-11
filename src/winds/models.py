import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

from .generators import WIND_GENERATOR_NAMES

# Create your models here.
class Timestamped(models.Model):
    """Abstract model to add timestamp fields"""
    created_at = models.DateTimeField(auto_now=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

def get_triple_0():
    return [0, 0, 0]
class WindGenParams(Timestamped):
    """Parameters used by the generator to generate trajectories of wind speed per spatial dimension (x,y,z) over time (t)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # flags to indicate generator
    is_windless = models.BooleanField(default=False)
    is_constant = models.BooleanField(default=False)
    is_oscillatory = models.BooleanField(default=False)
    is_lorenz = models.BooleanField(default=False)

    # Constant
    base_velocity = ArrayField(models.FloatField(), max_length=3, default=get_triple_0) # [x,y,z]

    # Oscillatory --> speed = base_speed + amplitude * cos(2𝜋*frequency*t + phase_offset)   ... for each of [x,y,z] directions
    frequency = ArrayField(models.FloatField(), max_length=3, default=get_triple_0) # [x,y,z]
    amplitude = ArrayField(models.FloatField(), max_length=3, default=get_triple_0) # [x,y,z]
    phase_offset = ArrayField(models.FloatField(), max_length=3, default=get_triple_0) # [x,y,z]

    # Lorenz
    rho = models.FloatField(null=True, default=0)
    sigma = models.FloatField(null=True, default=0)
    beta = models.FloatField(null=True, default=0)


class WindSpacetime(Timestamped):
    """Trajectories of wind speed per spatial dimension (x,y,z) over time (t) --> Table contains meta data, blob contains the actual time-trajectory data."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    generator_name = models.CharField(max_length=30, choices=WIND_GENERATOR_NAMES)
    generator_params = models.ForeignKey(WindGenParams, on_delete=models.CASCADE, null=True)
    duration = models.FloatField(default=100) # in seconds
    timestep = models.FloatField(default=0.01) # in seconds

    blob_filename = models.CharField(max_length=50, null=True) # filenames will be uuid plus extension... <uuid>.pkl ... so we expect 40 or so characters

