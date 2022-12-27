from django.db import models
from django.contrib.postgres.fields import ArrayField

from commons.models import Timestamped
from winds.models import WindGenParams, WindSpacetime

# Create your models here.
AIMING_GEOMETRY_CHOICES = [
    ('EulerAngles', 'EulerAngles'),
    ('Spherical', 'Spherical'),
    ('Cylindrical', 'Cylindrical'),
]
PROBABILITY_FUNCTION_CHOICES = [
    ('Uniform', 'Uniform'),
    ('Normal', 'Normal'),
    ('Log-normal', 'Log-normal'),
]

class BaseParams(models.Model):
    """Base parameters used in SimTrial and SimExperiment models"""
    # winds
    windgenparams = models.ForeignKey(WindGenParams, on_delete=models.CASCADE, null=True)
    windspacetime = models.ForeignKey(WindSpacetime, on_delete=models.CASCADE, null=True)

    # physics
    m = models.FloatField(default=.0456) # mass of the ball (kg)
    g = models.FloatField(default=-9.81) # gravitational constant (in +z direction)
    drag_coef = models.FloatField(default=0) # drag coefficient

    # parameters to tune the initial speed delivered to the ball
    prob_speed_fn_name = models.CharField(max_length=50, choices=PROBABILITY_FUNCTION_CHOICES)
    max_initial_speed = models.FloatField(null=True) # initial speed delivered in [0, max]
    prob_speed_center = models.FloatField(null=True)
    prob_speed_spread = models.FloatField(null=True)

    # parameters to tune the probability function for timing the hit
    prob_timing_fn_name = models.CharField(max_length=50, choices=PROBABILITY_FUNCTION_CHOICES)
    max_wait_time = models.FloatField(null=True)
    prob_timing_center = models.FloatField(null=True)
    prob_timing_spread = models.FloatField(null=True)

    # parameters to tune the probability function for aiming in 3-dimensional space
    prob_aiming_fn_name = models.CharField(max_length=50, choices=PROBABILITY_FUNCTION_CHOICES)
    prob_aiming_geometry = models.CharField(max_length=50, choices=AIMING_GEOMETRY_CHOICES)
    prob_aiming_X1_min = models.FloatField(null=True)
    prob_aiming_X1_max = models.FloatField(null=True)
    prob_aiming_X1_center = models.FloatField(null=True)
    prob_aiming_X1_spread = models.FloatField(null=True)
    prob_aiming_X2_min = models.FloatField(null=True)
    prob_aiming_X2_max = models.FloatField(null=True)
    prob_aiming_X2_center = models.FloatField(null=True)
    prob_aiming_X2_spread = models.FloatField(null=True)
    prob_aiming_X3_min = models.FloatField(null=True)
    prob_aiming_X3_max = models.FloatField(null=True)
    prob_aiming_X3_center = models.FloatField(null=True)
    prob_aiming_X3_spread = models.FloatField(null=True)

    # time resolution of the simulation
    timestep = models.FloatField() 

    class Meta:
        abstract = True

class SimTrial(BaseParams, Timestamped):
    """Single ball trajectory"""
    time_initial = models.FloatField()
    direction_initial = ArrayField(models.FloatField(), max_length=3) # unit vector
    speed_initial = models.FloatField()

    blob_filename = models.CharField(max_length=50, null=True)

class SimExperiment(BaseParams, Timestamped):
    """Collection of SimTrials for single parameter set"""
    is_control = models.BooleanField(default=False) # control will probably be uniform distribution (no target locality within timing, speed, or direction)
    simtrials = models.ManyToManyField(SimTrial)

# field_names = [f.__str__() for f in BaseParams._meta.get_fields()]
class DesignOfExperiments(Timestamped):
    """Collection of SimExperiments to map outcome over parameter landscape"""
    # Can I populate this Model's attribute names from BaseParams' field_names and assign different values... e.g. ArrayField
    # I want each parameter to have a 3-tuple corresponding to (start, end, num_points).
    placeholder = models.IntegerField()