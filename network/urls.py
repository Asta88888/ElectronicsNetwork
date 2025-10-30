from django.urls import path, include
from rest_framework.routers import SimpleRouter
from network.views import NetworkNodeViewSet
from network.apps import NetworkConfig

app_name = NetworkConfig.name

router = SimpleRouter()
router.register("", NetworkNodeViewSet, basename="network")
urlpatterns = [
    path("", include(router.urls))
]