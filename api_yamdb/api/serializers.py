from django.shortcuts import get_object_or_404
from rest_framework import serializers

from constants import LENGTH_CODE
from reviews.models import Category, Title, Genre, Review, Comment
from users.models import User
from .mixins import LookUpSlugFieldMixin


class CategorySerializer(serializers.ModelSerializer, LookUpSlugFieldMixin):
    """Сериализатор для модели категорий."""
    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer, LookUpSlugFieldMixin):
    """Сериализатор для модели жанров."""
    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели произведений."""
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    # TODO: rating
    rating = serializers.IntegerField(read_only=True)
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )

    def to_representation(self, instance):
        """Готовит данные для отправки в ответе."""
        representation = super().to_representation(instance)
        representation["category"] = {
            "name": instance.category.name,
            "slug": instance.category.slug,
        }
        representation["genre"] = [
            {
                "name": genre.name,
                "slug": genre.slug,
            }
            for genre in instance.genre.all()
        ]
        return representation


class CommentSerializers(serializers.ModelSerializer):
    """Сериализатор для модели Комментариев."""
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )
    review = serializers.SlugRelatedField(slug_field="text", read_only=True)

    class Meta:
        fields = ("id", "review", "author", "text", "pub_date")
        model = Comment


class ReviewSerializers(serializers.ModelSerializer):
    """Сериализатор для модели Отзывов."""
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )
    title = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        fields = ("id", "title", "text", "author", "score", "pub_date")
        model = Review

    def validate(self, data):
        """Проверка на то, чтобы пользователь оставлял только один отзыв."""
        if self.context.get("request").method != "POST":
            return data
        title_id = self.context.get("view").kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        author = self.context.get("request").user
        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError("Вы уже оставили отзыв!!!")
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
        if len(value) == LENGTH_CODE:
            return value
        raise serializers.ValidationError('Некорректный код подтверждения.')


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
        user = self.context['request'].user
        if user.is_staff:
            return value
        raise serializers.ValidationError(
            'Назначать роль моджет только администратор.'
        )
