from rest_framework import filters
# from .models import Recipe
# from django_filters.rest_framework import DjangoFilterBackend


class IngredientSearchFilter(filters.SearchFilter):
    search_param = 'name'


# class TagsFilterSet(filters.FilterSet):
#     championship = DjangoFilterBackend(field_name='tags__slug')

#     class Meta:
#         model = Recipe
#         fields = ['tags']
