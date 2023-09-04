from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    """
    Позволяет фильтровать объекты модели Title
    по поля genre, category, year, name.
    """
    genre = filters.CharFilter(field_name='genre__slug')
    category = filters.CharFilter(field_name='category__slug')
    year = filters.NumberFilter(field_name='year')
    name = filters.CharFilter(field_name='name')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'year']
