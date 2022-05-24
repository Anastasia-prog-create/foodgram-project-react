from rest_framework import filters
from .models import Recipe
from django_filters import FilterSet


class IngredientSearchFilter(filters.SearchFilter):
    search_param = 'name'


class RecipesFilter(FilterSet):
    tags = filters.django_filters.CharFilter(field_name='tags__slug') 

    class Meta:
        model = Recipe
        fields = ['tags', 'author']
