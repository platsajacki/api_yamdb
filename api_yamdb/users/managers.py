from typing import Any

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Кастомный менеджер для модели пользователя."""
    use_in_migrations: bool = True

    def _create_user(
            self, username: str, email: str,
            password: str = None, **extra_fields: Any
    ):
        """
        Создает и сохраняет пользователя с username, email,
        и password для суперпользователя.
        """
        if not username:
            raise ValueError('Необходимо указать имя пользователя.')
        if not email:
            raise ValueError('Необходимо указать электронную почту.')
        email: str = self.normalize_email(email)
        user: self.model = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        if extra_fields.get('is_superuser'):
            # Пароль есть только у суперпользователя
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self, username: str, email: str,
            password: str = None, **extra_fields: Any
    ):
        """Создает и сохраняет обычного пользователя."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
            self, username: str, email: str,
            password: str = None, **extra_fields: Any
    ):
        """Создает и сохраняет суперпользователя."""
        extra_fields.setdefault(
            'is_staff', True
        )
        extra_fields.setdefault(
            'is_superuser', True
        )
        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Суперпользователь должен иметь is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Суперпользователь должен иметь is_superuser=True.'
            )
        return self._create_user(username, email, password, **extra_fields)
