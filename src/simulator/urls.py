from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RunExperimentView

urlparameters = [
    path('run-experiment', RunExperimentView.as_view()),
]