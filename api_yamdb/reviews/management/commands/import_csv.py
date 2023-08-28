from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import Category
import csv


DATA_DIR: str = settings.BASE_DIR / "static/data"


class Command(BaseCommand):
    help = "Импортирует данные из файла category.csv в таблицу Category"

    def handle(self, *args, **options):
        with open(
            f"{DATA_DIR}/category.csv", "r"
        ) as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                category_obj, created = Category.objects.get_or_create(
                    name=row[0], slug=row[1]
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully imported category: {row[0]}"
                        )
                    )
                else:
                    self.stdout.write(f"Category already exists: {row[1]}")
