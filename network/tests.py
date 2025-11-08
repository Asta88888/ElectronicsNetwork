from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from network.models import NetworkNode, Product

User = get_user_model()


class NetworkAPITestCase(APITestCase):
    """
    Тестирование API для сети поставщиков.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            email="test@example.com",
            password="test101208",
            is_active=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.iphone = Product.objects.create(name="iPhone", model="15 Pro", release_date="2025-11-08")
        self.macbook = Product.objects.create(name="MacBook", model="M3 Pro", release_date="2025-11-08")

        self.iphone_factory = NetworkNode.objects.create(
            name="Apple iPhone Factory",
            email="iphone_factory@apple.com",
            country="США",
            city="Нью-Йорк",
            street="Iphone street",
            house_number="1"
        )
        self.iphone_factory.products.add(self.iphone)

        self.mac_factory = NetworkNode.objects.create(
            name="Apple MacBook Factory",
            email="mac_factory@apple.com",
            country="США",
            city="Нью-Йорк",
            street="Macbook street",
            house_number="2"
        )
        self.mac_factory.products.add(self.macbook)

        self.ip_shop = NetworkNode.objects.create(
            name="SPB iShop",
            email="ishop_spb@example.com",
            country="Россия",
            city="Санкт-Петербург",
            street="Невский проспект",
            house_number="24",
            supplier=self.iphone_factory
        )
        self.ip_shop.products.add(self.iphone)

    def test_get_products_list(self):
        """Проверка получения списка продуктов."""
        url = reverse('network:product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_network_nodes(self):
        """Проверка получения всех звеньев сети."""
        url = reverse('network:node-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_country(self):
        """Фильтрация по стране."""
        url = reverse('network:node-list')
        response = self.client.get(url, {'country': 'Россия'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'SPB iShop')

    def test_create_node_with_supplier(self):
        """Создание нового ИП с поставщиком."""
        url = reverse('network:node-list')
        data = {
            "name": "SPB MacShop",
            "email": "macshop_spb@example.com",
            "country": "Россия",
            "city": "Санкт-Петербург",
            "street": "Невский проспект",
            "house_number": "12",
            "products": [self.macbook.id],
            "supplier": self.mac_factory.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['supplier_name'], "Apple MacBook Factory")

    def test_permissions_for_inactive_user(self):
        """Неактивный пользователь не может выполнять запросы."""
        inactive_user = User.objects.create_user(
            username="inactive",
            email="inactive@example.com",
            password="nopass",
            is_active=False
        )
        client = APIClient()
        client.force_authenticate(user=inactive_user)

        url = reverse('network:product-list')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
