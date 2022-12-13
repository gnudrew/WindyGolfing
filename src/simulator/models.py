from django.db import models

from commons.models import Timestamped

# Create your models here.
def get_prob_aiming_fn_choices():
    choices = [
        ('EulerAngles', 'EulerAngles'),
        ('SphericalCoordinates', 'SphericalCoordinates'),
        ('CylindricalCoordinates', 'CylindricalCoordinates')
    ]
    return choices
class BaseParams(models.Model):
    """Base parameters used in SimTrial and SimExperiment models"""
    g = models.FloatField() # gravitational constant (assume -z direction)
    max_initial_speed = models.FloatField()
    
    # parameters to tune the probability function for timing
    max_wait_time = models.FloatField()
    prob_timing_center = models.FloatField()
    prob_timing_spread = models.FloatField()

    # parameters to tune the probability function for aiming in 3-dimensional space
    prob_aiming_function = models.CharField(max_length=20, choices=get_prob_aiming_fn_choices)
    prob_aiming_X1_center = models.FloatField()
    prob_aiming_X1_spread = models.FloatField()
    prob_aiming_X2_center = models.FloatField()
    prob_aiming_X2_spread = models.FloatField()
    prob_aiming_X3_center = models.FloatField()
    prob_aiming_X3_spread = models.FloatField()

    timestep = models.FloatField() # time resolution of the simulation

    class Meta:
        abstract = True

class SimTrial(BaseParams, Timestamped):
    blob_filename = models.CharField(max_length=50, null=True)

class SimExperiment(BaseParams, Timestamped):
    simtrials = models.ManyToManyField()