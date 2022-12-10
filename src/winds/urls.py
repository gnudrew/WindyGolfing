from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import WindGeneratorParametersViewSet

router = DefaultRouter()
router.register('wind-gen-params', WindGeneratorParametersViewSet)

urlpatterns = router.urls

# urlpatterns = [
#     path('', include(router.urls))
# ]