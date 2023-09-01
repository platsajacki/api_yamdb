from typing import Any

from django.core.cache import cache
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import Token, RefreshToken
from rest_framework import status

from .serializers import (
    UserRegistrationSerializer, UserTokenSerializer, UserSerializer
)
from constants import LENGTH_CODE
from users.models import User


class UserRegistrationView(generics.CreateAPIView):
    """Представление для регистрации пользователя."""
    serializer_class = UserRegistrationSerializer

    def perform_create(
            self, serializer: UserRegistrationSerializer
    ) -> Response:
        """Попытка создания пользователя и отправки кода подтверждения."""
        serializer.is_valid(raise_exception=True)
        try:
            confirmation_code: str = get_random_string(length=LENGTH_CODE)
            user, _ = User.objects.get_or_create(
                username=serializer.data.get('username'),
                email=serializer.data.get('email')
            )
            cache.set(
                str(user.id),
                confirmation_code
            )
            self.send_confirmation_code(user.email, confirmation_code)
            return user
        except IntegrityError as error:
            raise ValidationError(
                'Такое имя пользователя уже существует.'
                if 'username' in str(error) else
                'Пользователь с таким электронным адресом уже существует.'
            )
        except APIException as error:
            raise APIException(
                f'Произошла ошибка при регистрации пользователя: {error}'
            )

    def send_confirmation_code(
            self, email: str, confirmation_code: str
    ) -> None:
        """Отправка кода подтверждения по электронной почте."""
        subject: str = 'Код подтверждения регистрации в YaMDB'
        message: str = f'Ваш код подтверждения: {confirmation_code}'
        from_email: str = 'yamdb@gmail.com'
        recipient_list: list[str] = [email]
        send_mail(subject, message, from_email, recipient_list)


class UserTokenView(generics.CreateAPIView):
    """Получение пользователем JWT-токена."""
    serializer_class = UserTokenSerializer

    def create(
            self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        """Обработка POST-запроса на получение JWT-токена."""
        serializer: dict[str, str] = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username: str = request.data['username']
        confirmation_code: str = request.data['confirmation_code']
        user: User = get_object_or_404(
            User, username=username
        )
        if confirmation_code == cache.get(str(user.id)):
            refresh: Token = RefreshToken.for_user(user)
            return Response(
                {'token': str(refresh.access_token)}
            )
        return Response(
            {'confirmation_code': ['Код подтверждения введен неверно.']},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects
    lookup_field = 'username'
    http_method_names = [
        'get', 'post', 'patch', 'delete'
    ]
    permission_classes = [IsAdminUser]
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False, methods=['get', 'post'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
