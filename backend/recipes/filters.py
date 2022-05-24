from rest_framework import filters
from .models import Recipe
from django_filters.rest_framework import FilterSet


class IngredientSearchFilter(filters.SearchFilter):
    search_param = 'name'


class RecipesFilter(FilterSet):
    tags = filters.CharFilter(field_name='last_login') 

    class Meta:
        model = Recipe
        fields = ['tags', 'author']
