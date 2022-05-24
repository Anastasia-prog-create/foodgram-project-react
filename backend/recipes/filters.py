from rest_framework import filters
from .models import Recipe, Tag
import django_filters as filters


class IngredientSearchFilter(filters.SearchFilter):
    search_param = 'name'


class RecipesFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        name='tags__slug',
        to_field_name='tags',
        lookup_type='in',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ['author',]
