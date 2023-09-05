from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View

from constants import ADMIN, MODERATOR


class IsAdminOnly(permissions.BasePermission):
    """
    Только пользователи с правами администратора (is_staff)
    или ролью 'admin' имеют разрешение на доступ.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        """Проверяет разрешение доступа на уровне представления."""
        return (
            request.user.is_staff
            or request.user.role == ADMIN
        )


class IsAuthor(permissions.BasePermission):
    """Автор объекта имеет разрешение на доступ."""
    def has_object_permission(
            self, request: Request, view: View, obj: Model
    ) -> bool:
        """Проверяет разрешение доступа к объекту."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and obj.author == request.user
        )


class IsAdminObject(permissions.BasePermission):
    """
    Пользователи с правами администратора (is_staff)
    или ролью 'admin' имеют разрешение на доступ.
    """
    def has_object_permission(
            self, request: Request, view: View, obj: Model
    ) -> bool:
        """Проверяет разрешение доступа к объекту."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.role == ADMIN
                or request.user.is_staff
            )
        )


class IsModerator(permissions.BasePermission):
    """Пользователь с ролью 'Moderator' имеет разрешение на доступ."""
    def has_object_permission(
            self, request: Request, view: View, obj: Model
    ) -> bool:
        """Проверяет разрешение доступа к объекту."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == MODERATOR
        )
