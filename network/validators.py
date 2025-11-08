from django.core.exceptions import ValidationError


def validate_supplier_chain(instance):
    """
    Проверяет нет ли циклов в цепочке поставщиков.
    """
    supplier = instance.supplier
    seen = set()

    while supplier is not None:
        if supplier.pk == instance.pk:
            raise ValidationError("Обнаружен цикл: объект не может быть своим собственным поставщиком.")
        if supplier.pk in seen:
            raise ValidationError("Обнаружен цикл в цепочке поставщиков.")
        seen.add(supplier.pk)
        supplier = supplier.supplier
