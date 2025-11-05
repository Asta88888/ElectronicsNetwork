from rest_framework.exceptions import ValidationError
from network.validators import validate_supplier_chain


def calculate_level(instance):
    """
    Вычисляет уровень звена цепи.
    """
    validate_supplier_chain(instance)
    level = 0
    supplier = instance.supplier
    seen = set()

    while supplier is not None:
        if supplier.pk in seen:
            raise ValidationError
        seen.add(supplier.pk)
        level += 1
        supplier = supplier.supplier
    return level
