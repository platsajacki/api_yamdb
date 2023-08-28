import datetime as dt

from django.db import models
from django.core.validators import MaxValueValidator


class Category(models.Model):
    """
    Модель для хранения информации о категории произведения.
    """
    name = models.CharField("Название", max_length=255)
    slug = models.SlugField("Слаг", max_length=255, unique=True)

    def __str__(self) -> str:
        """
        Возвращает строковое представление категории (ее название).
        """
        return self.name


class Genre(models.Model):
    """
    Модель для хранения информации о жанре произведения.
    """
    name = models.CharField("Название", max_length=255)
    slug = models.SlugField("Слаг", max_length=255)

    def __str__(self) -> str:
        """
        Возвращает строковое представление жанра (его название).
        """
        return self.name


class Title(models.Model):
    """
    Модель для хранения информации о произведении.
    """
    name = models.CharField("Название", max_length=255)
    year = models.PositiveSmallIntegerField(
        "Год выхода",
        validators=[
            MaxValueValidator(dt.datetime.now().year),
        ],
    )
    description = models.TextField("Описание", blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="titles",
        verbose_name="Категория",
    )
    genre = models.ManyToManyField(Genre, through="GenreTitle")

    def __str__(self) -> str:
        """
        Возвращает строковое представление произведения (его название).
        """
        return self.name


class GenreTitle(models.Model):
    """
    Промежуточная модель для хранения ключей genre и title
    """
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True, verbose_name="Жанр"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name="Произведение"
    )

    def __str__(self) -> str:
        """
        Возвращает строковое представление жанра и произведения
        """
        return f"{self.title} - {self.genre}"
