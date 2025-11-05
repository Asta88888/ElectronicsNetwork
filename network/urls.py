from django.urls import path, include
from rest_framework.routers import SimpleRouter
from network.views import NetworkNodeViewSet, ProductViewSet
from network.apps import NetworkConfig

app_name = NetworkConfig.name

router = SimpleRouter()
router.register(r"nodes", NetworkNodeViewSet, basename="node")
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls))
]
