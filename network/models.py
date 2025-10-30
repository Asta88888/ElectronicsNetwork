from django.db import models
from network.validators import validate_supplier_chain
from network.services import calculate_level


class Product(models.Model):
    """
    Модель продукта электроники.
    Хранит информацию о товарах, производимых или реализуемых сетью.
    """
    name = models.CharField(max_length=300, verbose_name="Название")
    model = models.CharField(max_length=300, verbose_name="Модель")
    release_date = models.DateTimeField(verbose_name="Дата выхода на рынок")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        """
        Возвращает читаемое представление продукта.
        """
        return f"{self.name} ({self.model})"


class NetworkNode(models.Model):
    """
    Модель звена торговой сети (завод, сеть, индивидуальный предприниматель).
    """
    LEVEL_CHOICES = (
        (0, "Завод"),
        (1, "Розничная сеть"),
        (2, "Индивидуальный предприниматель"),
    )
    name = models.CharField(max_length=200, verbose_name="Название")
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=200, verbose_name="Страна")
    city = models.CharField(max_length=200, verbose_name="Город")
    street = models.CharField(max_length=200, verbose_name="Улица")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома")
    products = models.ManyToManyField(
        Product,
        related_name="network_nodes",
        blank=True,
        verbose_name="Продукты"
    )
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
        verbose_name="Поставщик",
    )
    debt = models.DecimalField(max_length=12, decimal_places=2, default=0, verbose_name="Задолженность")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    level = models.PositiveIntegerField(default=0, choices=LEVEL_CHOICES, editable=False, verbose_name="Уровень иерархии")

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"

    def clean(self):
        """
        Проверка корректности цепочки поставщиков.
        """
        validate_supplier_chain(self)

    def save(self, *args, **kwargs):
        """
        При сохранении объекта автоматически рассчитывает уровень узла в иерархии.
        """
        self.level = calculate_level(self)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Возвращает читаемое название звена с указанием типа.
        """
        return f"{self.name} ({self.get_level_display()})"
