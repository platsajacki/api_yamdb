from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Title, Genre, GenreTitle, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    # TODO: title rating
    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer(read_only=True)

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

    def create(self, validated_data):
        genres = validated_data.pop("genre")
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre, _ = Genre.objects.get_or_create(**genre)
            GenreTitle.objects.create(genre=current_genre, title=title)
        return title


class CommentSerializers(serializers.ModelSerializer):
    """Сеарилизатор для модели Комментариев."""
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field="text",
        read_only=True
    )

    class Meta:
        fields = "__all__"
        models = Comment


class ReviewSerializers(serializers.ModelSerializer):
    """Сеарилизатор для модели Отзывов."""
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True
    )

    class Meta:
        fields = "__all__"
        models = Review

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
