from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View
from django.db.models import Model


class AllowAdminOrAnonymousPermission(permissions.BasePermission):
    """
    Разрешает доступ для анонимных пользователей
    или пользователей с ролью admin.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        """Проверяет разрешение доступа на уровне представления."""
        return request.user.is_anonymous or request.user.role == 'admin'


class AuthorModeratorAdminPermission(permissions.BasePermission):
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
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
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
            or request.user.role == 'admin'
        )
