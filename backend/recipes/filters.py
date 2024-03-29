from rest_framework import filters

from .models import Recipe, Tag
import django_filters as filter


class IngredientSearchFilter(filters.SearchFilter):
    search_param = 'name'


class RecipesFilter(filter.FilterSet):
    tags = filter.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags']
