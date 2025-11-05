from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Команда для создания суперпользователя.
    """
    def handle(self, *args, **kwargs):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username="admin",
            email="admin@example.com",
            defaults={
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            }
        )
        if created:
            user.set_password("101208")
            message = f"Создан новый суперпользователь: {user.email}"
        else:
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            message = f"Пользователь {user.email} уже существует, права обновлены."
        user.save()
        self.stdout.write(self.style.SUCCESS(message))
