from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import WindGeneratorParametersViewSet

router = DefaultRouter()
router.register('wind-gen-params', WindGeneratorParametersViewSet, basename='wind-gen-params')

urlpatterns = router.urls

# urlpatterns = [
#     path('', include(router.urls))
# ]