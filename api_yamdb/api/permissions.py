from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View


class AllowAdminOrAnonymousPermission(permissions.BasePermission):
    """
    Разрешает доступ для анонимных пользователей
    или пользователей с ролью admin.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_anonymous or request.user.role == 'admin'


class AuthorModeratorAdminPermission(permissions.BasePermission):
    """Для aутентифициризванныx пользователей с ролью Admin,Moderator
    и Автору.Либо аннониму только безопасные запросы."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
            )
        )
