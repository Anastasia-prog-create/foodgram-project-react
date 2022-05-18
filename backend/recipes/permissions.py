from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorOrReadOnly(BasePermission):
    """Класс разрешений на действия с рецептами."""

    def has_permission(self, request, view):
        """Проверка на аутентификацию."""
        return (
            request.user.is_authenticated
            or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        """Проверка на авторство."""
        return (
            obj.author == request.user
            or request.method in SAFE_METHODS
        )
