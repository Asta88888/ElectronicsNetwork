from rest_framework import permissions


class IsActiveUser(permissions.BasePermission):
    """
    Разрешает доступ к API только активным пользователям.
    Пользователь должен быть аутентифицирован и иметь is_active = True
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_active)
