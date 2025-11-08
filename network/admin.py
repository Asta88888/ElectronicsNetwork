from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from network.models import NetworkNode, Product

User = get_user_model()

if not admin.site.is_registered(User):
    @admin.register(User)
    class UserAdmin(BaseUserAdmin):
        """
        Кастомный UserAdmin для работы с моделью пользователя по email.
        """
        model = User
        list_display = ("email", "is_staff", "is_active", "is_superuser")
        list_filter = ("is_staff", "is_active", "is_superuser")
        search_fields = ("email",)
        ordering = ("email",)
        fieldsets = (
            (None, {"fields": ("email", "password")}),
            ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active")}),
            ("Groups & User Permissions", {"fields": ("groups", "user_permissions")}),
        )
        add_fieldsets = (
            (None, {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_superuser", "is_active"),
            }),
        )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админка для продуктов.
    """
    list_display = ("name", "model", "release_date")
    search_fields = ("name", "model")
    ordering = ("release_date",)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Админка для звеньев торговой сети.
    """
    list_display = (
        "name",
        "email",
        "city",
        "country",
        "supplier_name",
        "debt",
        "level",
        "created_at",
    )
    list_filter = ("city", "country", "level")
    search_fields = ("name", "email", "city", "country")
    readonly_fields = ("created_at", "level")
    actions = ["clear_debt"]

    def supplier_name(self, obj):
        """
        Отображает имя поставщика.
        """
        return obj.supplier.name if obj.supplier else "-"
    supplier_name.short_description = "Поставщик"

    @admin.action(description="Очистить задолженность перед поставщиком")
    def clear_debt(self, request, queryset):
        """
        Обнуляет задолженность у выбранных звеньев.
        """
        updated = queryset.update(debt=0)
        self.message_user(request, f"Задолженность очищена у {updated} объектов.")
