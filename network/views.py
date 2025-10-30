from rest_framework.viewsets import ModelViewSet
from network.models import Product, NetworkNode
from network.serializers import ProductSerializer, NetworkNodeSerializer
from rest_framework import filters
from network.permissions import IsActiveUser
from django_filters.rest_framework import DjangoFilterBackend


class ProductViewSet(ModelViewSet):
    """
    ViewSet для управления продуктами электроники.
    Доступ разрешён только активным пользователям.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "model"]
    ordering_fields = ["release_date"]


class NetworkNodeViewSet(ModelViewSet):
    """
    ViewSet для управления звеньями торговой сети (завод, розничная сеть, индивидуальный предприниматель).
    Позволяет выполнять CRUD-операции, фильтровать по стране, доступ разрешён только активным пользователям.
    """
    queryset = NetworkNode.objects.select_related("supplier").prefetch_related("products")
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["country"]
    search_fields = ["name", "city", "country"]
    ordering_fields = ["created_at", "level"]
