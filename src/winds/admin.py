from django.contrib import admin

from .models import WindGenParams,WindSpacetime

# Register your models here.
admin.site.register(WindGenParams)
admin.site.register(WindSpacetime)