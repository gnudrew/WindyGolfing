from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import WindGeneratorParametersViewSet, WindSpacetimeViewSet

router = DefaultRouter()
router.register('wind-gen-params', WindGeneratorParametersViewSet)
router.register('wind-spacetimes', WindSpacetimeViewSet)

urlpatterns = router.urls

# urlpatterns = [
#     path('', include(router.urls))
# ]