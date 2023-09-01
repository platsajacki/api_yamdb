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
