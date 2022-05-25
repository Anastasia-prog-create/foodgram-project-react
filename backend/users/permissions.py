from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOrUserOrReadOnly(BasePermission):
    """Класс разрешений на действия с User."""
    def has_permission(self, request, view):
        return(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.method in SAFE_METHODS
                or obj == request.user
                or request.user.is_superuser
            )
