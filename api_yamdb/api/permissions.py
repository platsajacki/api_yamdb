from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View

from constants import ADMIN, MODERATOR


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):
    """
    Позволяет доступ аутентифицированным пользователям с ролью 'Admin',
    'Moderator' или автору объекта. Анонимным пользователям разрешены
    только безопасные запросы.
    """
    def has_object_permission(
            self, request: Request, view: View, obj: Model
    ) -> bool:
        """Проверяет разрешение доступа к объекту."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.role == MODERATOR
                or request.user.role == ADMIN
            )
        )


class IsAdminOrRoleIsAdmin(permissions.BasePermission):
    """
    Пользователи с правами администратора (is_staff)
    или ролью 'admin' имеют разрешение на доступ.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        """Проверяет разрешение доступа на уровне представления."""
        return (
            request.user.is_staff
            or request.user.role == ADMIN
        )
