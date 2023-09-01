from rest_framework import mixins, viewsets


class LookUpSlugFieldMixin:
    """
    Добавляет поле 'lookup_field' со значением 'slug'
    для создания url-путей с использованием 'slug' вместо 'id'.
    """
    class Meta:
        abstract = True
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Миксин для добавления возможности создания,
    получения списка и удаления объектов модели.
    """
    ...
