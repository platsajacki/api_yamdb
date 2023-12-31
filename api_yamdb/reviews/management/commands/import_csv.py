import csv
from typing import Any

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models

from reviews.models import Category, Title, Genre, TitleGenre, Comment, Review

DATA_DIR: str = f'{settings.BASE_DIR}/static/data'
User = get_user_model()


class Command(BaseCommand):
    """Импортирует данные из csv-файлов в базу данных."""
    help: str = 'Импортирует данные из csv-файлов в базу данных'

    def handle(self, *args: Any, **options: Any) -> None:
        """Вызов и обработка всех команд импорта из csv-файлов."""
        self.import_users()
        self.import_categories()
        self.import_genres()
        self.import_titles()
        self.import_reviews()
        self.import_comments()
        self.import_genre_title()

    def import_data_from_csv(
        self,
        file_path: str,
        model_class: models.Model,
        field_names: list[str],
    ) -> None:
        """Импортирует данные из csv-файла в базу данных."""
        with open(file_path, 'r') as csv_file:
            reader: csv.reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                data: dict[str, str] = dict(zip(field_names, row))

                model_exists: bool = model_class.objects.filter(
                    id=data['id']
                ).exists()

                if not model_exists:
                    if 'author' in field_names:
                        author_id: int = data.pop('author')
                        author: User = User.objects.get(id=author_id)
                        data['author'] = author

                    model_class.objects.create(**data)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Данные успешно импортированы: {data["id"]}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Данные уже существуют: {data["id"]}'
                        )
                    )

    def import_categories(self) -> None:
        """Импортирует категории из файла category.csv."""
        file_path: str = f'{DATA_DIR}/category.csv'
        field_names: list[str] = ['id', 'name', 'slug']
        self.import_data_from_csv(file_path, Category, field_names)

    def import_genres(self) -> None:
        """Импортирует жанры из файла genre.csv."""
        file_path: str = f'{DATA_DIR}/genre.csv'
        field_names: list[str] = ['id', 'name', 'slug']
        self.import_data_from_csv(file_path, Genre, field_names)

    def import_titles(self) -> None:
        """Импортирует произведения из файла titles.csv."""
        file_path: str = f'{DATA_DIR}/titles.csv'
        field_names: list[str] = ['id', 'name', 'year', 'category_id']
        self.import_data_from_csv(file_path, Title, field_names)

    def import_reviews(self) -> None:
        """Импортирует отзывы из файла review.csv."""
        file_path: str = f'{DATA_DIR}/review.csv'
        field_names: list[str] = [
            'id',
            'title_id',
            'text',
            'author',
            'score',
            'pub_date',
        ]
        self.import_data_from_csv(file_path, Review, field_names)

    def import_comments(self) -> None:
        """Импортирует комментарии из файла comments.csv."""
        file_path: str = f'{DATA_DIR}/comments.csv'
        field_names: list[str] = [
            'id',
            'review_id',
            'text',
            'author',
            'pub_date',
        ]
        self.import_data_from_csv(file_path, Comment, field_names)

    def import_genre_title(self) -> None:
        """Импортирует связь жанров и произведений из файла genre_title.csv."""
        file_path: str = f'{DATA_DIR}/genre_title.csv'
        field_names: list[str] = ['id', 'title_id', 'genre_id']
        self.import_data_from_csv(file_path, TitleGenre, field_names)

    def import_users(self) -> None:
        """Импортирует пользователей из файла users.csv."""
        file_path: str = f'{DATA_DIR}/users.csv'
        field_names: list[str] = [
            'id',
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name',
        ]
        self.import_data_from_csv(file_path, User, field_names)
