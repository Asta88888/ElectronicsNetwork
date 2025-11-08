from rest_framework import serializers

from network.models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения, создания и редактирования данных о продукте в API.
    """
    class Meta:
        model = Product
        fields = ["id", "name", "model", "release_date"]
        read_only_fields = ["id"]


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели NetworkNode.
    Поле "Задолженности"("debt") доступно только для чтения через API.
    Включает связанные продукты
    """
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all(),
        required=False
    )
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            "id",
            "name",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "products",
            "supplier",
            "supplier_name",
            "debt",
            "created_at",
            "level",
        ]
        read_only_fields = ["id", "debt", "created_at", "level", "supplier_name"]

        def create(self, validated_data):
            """
            Создаёт новый узел сети.
            """
            return super().create(validated_data)

        def update(self, instance, validated_data):
            """
            Обновляет узел сети, не трогая поле 'debt'.
            """
            validated_data.pop("debt", None)
            return super().update(instance, validated_data)
