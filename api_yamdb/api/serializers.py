from typing import Any

from django.core.cache import cache
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Comment, Genre, Review, Title

from .mixins import LookUpSlugFieldMixin
from constants import LENGTH_CODE
from users.models import User


class CategorySerializer(serializers.ModelSerializer, LookUpSlugFieldMixin):
    """Сериализатор для модели категорий."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer, LookUpSlugFieldMixin):
    """Сериализатор для модели жанров."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели произведений."""
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(read_only=True)
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def to_representation(self, instance: Title) -> dict[str, str]:
        """Готовит данные для отправки в ответе."""
        representation: dict[str, str] = super().to_representation(instance)
        representation['category'] = {
            'name': instance.category.name,
            'slug': instance.category.slug,
        }
        representation['genre'] = [
            {
                'name': genre.name,
                'slug': genre.slug,
            }
            for genre in instance.genre.all()
        ]
        return representation


class CommentSerializers(serializers.ModelSerializer):
    """Сериализатор для модели Комментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comment


class ReviewSerializers(serializers.ModelSerializer):
    """Сериализатор для модели Отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """Проверка на то, чтобы пользователь оставлял только один отзыв."""
        if self.context.get('request').method != 'POST':
            return data
        title_id: int = self.context.get('view').kwargs.get('title_id')
        author: User = self.context.get('request').user
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError('Вы уже оставили отзыв!!!')
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = (
            'username',
            'email'
        )

    def create(self, validated_data: dict[str, Any]) -> User:
        """Создает нового пользователя на основе переданных данных."""
        try:
            user, _ = User.objects.get_or_create(
                username=validated_data.get('username'),
                email=validated_data.get('email'),
            )
        except IntegrityError as error:
            raise ValidationError(
                'Такое имя пользователя уже существует.'
                if 'username' in str(error)
                else 'Пользователь с таким электронным адресом уже существует.'
            )
        return user

    def validate_username(self, value: str) -> str:
        """Проверка имени пользователя на недопустимые значения."""
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" недопустимо.'
            )
        return value


class UserTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для подтверждения токенов пользователя."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )

    def validate_confirmation_code(self, value: str) -> str:
        """Проверка кода подтверждения."""
        username: str = self.context.get('request').data.get('username')
        if len(value) == LENGTH_CODE and value == cache.get(username):
            return value
        raise serializers.ValidationError('Код подтверждения введен неверно.')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки запросов к модели User."""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_role(self, value: str) -> str:
        """Проверяет, имеет ли текущий пользователь право назначать роли."""
        user: User = self.context['request'].user
        if user.is_staff or user.role == 'admin':
            return value
        raise serializers.ValidationError(
            'Назначать роль моджет только администратор.'
        )
