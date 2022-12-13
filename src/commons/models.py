from django.db import models

class Timestamped(models.Model):
    """Abstract model to add timestamp fields"""
    created_at = models.DateTimeField(auto_now=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
