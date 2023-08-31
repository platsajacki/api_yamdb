from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

ROLE_CHOICES = [
    ("user", "Пользователь"),
    ("moderator", "Модератор"),
    ("admin", "Администратор"),
]


class User(AbstractUser):
    """Кастомная модель пользователя."""
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
        choices=ROLE_CHOICES,
        default='user'
    )

    REQUIRED_FIELDS = ["email", ]

    objects = UserManager()
