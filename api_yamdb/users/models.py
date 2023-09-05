from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager
from constants import USER, MODERATOR, ADMIN


class User(AbstractUser):
    """Кастомная модель пользователя."""
    class Role(models.TextChoices):
        """Перечисление для ролей пользователей."""
        USER = USER, 'Пользователь'
        ADMIN = ADMIN, 'Админ'
        MODERATOR = MODERATOR, 'Модератор'

    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=254
    )
    bio = models.TextField(
        'О себе',
        max_length=512,
        blank=True, null=True
    )
    role = models.CharField(
        'Роль',
        max_length=10,
        choices=Role.choices,
        default=Role.USER
    )

    objects = UserManager()
