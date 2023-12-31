import datetime as dt

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .abstracts import BaseNameSlugModel
from users.models import User


class Category(BaseNameSlugModel):
    """Модель для хранения информации о категории произведения."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseNameSlugModel):
    """Модель для хранения информации о жанре произведения."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель для хранения информации о произведении."""
    name = models.CharField('Название', max_length=256)
    year = models.PositiveSmallIntegerField(
        'Год выхода',
        validators=[
            MaxValueValidator(dt.datetime.now().year),
        ],
    )
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(Genre, through='TitleGenre')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        """Возвращает строковое представление произведения (его название)."""
        return self.name


class TitleGenre(models.Model):
    """Промежуточная модель для хранения ключей genre и title."""
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True, verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение'
    )

    def __str__(self) -> str:
        """Возвращает строковое представление жанра и произведения."""
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    """Модель для отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=(MinValueValidator(1), MaxValueValidator(10)),
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='Unique_review'
            ),
        )
        default_related_name = 'reviews'

    def __str__(self) -> str:
        """Возвращает строковое представление отзыва."""
        return self.text


class Comment(models.Model):
    """Модель для комментариев."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self) -> str:
        """Возвращает строковое представление комментария."""
        return self.text
