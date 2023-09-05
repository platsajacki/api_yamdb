from django.db import models


class BaseNameSlugModel(models.Model):
    """Абстрактная базовая модель с полями name и slug."""
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """Возвращает строковое представление объекта (его название)."""
        return self.name
