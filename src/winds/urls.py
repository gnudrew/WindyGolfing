from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import WindGenParamsViewSet, WindSpacetimeViewSet

router = DefaultRouter()
router.register('wind-gen-params', WindGenParamsViewSet)
router.register('wind-spacetimes', WindSpacetimeViewSet)

urlpatterns = router.urls

# urlpatterns = [
#     path('', include(router.urls))
# ]