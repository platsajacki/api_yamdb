from rest_framework import viewsets, mixins
from rest_framework.exceptions import MethodNotAllowed

from .serializers import TitleSerializer, CategorySerializer, GenreSerializer
from reviews.models import Title, Category, Genre


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Миксин для добавления возможности создания,
    получения списка и удаления объектов модели
    """

    ...


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для работы с объектами модели Title"""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def update(self, request, *args, **kwargs):
        """Запрещает использовать метод PUT"""
        if request.method == "PUT":
            raise MethodNotAllowed(request.method)
        return super().update(request, *args, **kwargs)


class CategoryViewSet(CreateListDestroyViewSet):
    """Представление для работы с объектами модели Category"""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "slug"


class GenreViewSet(CreateListDestroyViewSet):
    """Представление для работы с объектами модели Genre"""

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    lookup_field = "slug"
