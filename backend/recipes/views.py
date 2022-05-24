from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from api.serializers import (FavoriteANDShoppingListSerializer,
                             IngredientSerializer,
                             RecipeCreateUpdateSerializer, RecipeGETSerializer,
                             TagSerializer)

from .filters import IngredientSearchFilter
from .models import (FavoriteList, Ingredient, Recipe, RecipeIngredients,
                     ShoppingCart, Tag)
from .permissions import AuthorOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter, )
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,) #TagsFilterSet)
    filterset_fields = ('author',)

    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
        )
        tags = self.request.query_params.get('tags')
        if tags:
            queryset = queryset.filter(tags__slug=tags)
        if is_favorited:
            recipes_id = FavoriteList.objects.filter(
                user=self.request.user
            ).values('recipe')
            queryset = Recipe.objects.filter(
                id__in=(map(lambda x: x['recipe'], recipes_id))
            )
        if is_in_shopping_cart:
            recipes_id = ShoppingCart.objects.filter(
                user=self.request.user
            ).values('recipe')
            queryset = Recipe.objects.filter(
                id__in=(map(lambda x: x['recipe'], recipes_id))
            )
        return queryset

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return RecipeCreateUpdateSerializer
        return RecipeGETSerializer

    def perform_create(self, serializer):
        """Метод для заполнения поля user."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed(request.method)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(permissions.IsAuthenticated,))
    def favorite(self, request, pk):
        if request.method == 'POST':
            try:
                favorite = FavoriteList.objects.create(
                    user=self.request.user,
                    recipe_id=pk
                )
                serializer = FavoriteANDShoppingListSerializer(favorite.recipe)
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except:
                return Response(
                    {'detail': 'Рецепт уже находится в избранном.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        if request.method == 'DELETE':
            try:
                favorite = FavoriteList.objects.get(
                    user=self.request.user,
                    recipe_id=pk
                )
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response(
                    {'detail': 'Рецепт не найден в избранном.'},
                    status=status.HTTP_400_BAD_REQUEST
                    )

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(permissions.IsAuthenticated, ))
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            try:
                cartitem = ShoppingCart.objects.create(
                    user=self.request.user,
                    recipe_id=pk
                )
                serializer = FavoriteANDShoppingListSerializer(cartitem.recipe)
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except:
                return Response(
                    {'detail': 'Рецепт уже находится в корзине.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        if request.method == 'DELETE':
            try:
                cartitem = get_object_or_404(
                    ShoppingCart, user=self.request.user, recipe_id=pk
                )
                cartitem.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response(
                    {'detail': 'Рецепт не найден в корзине.'},
                    status=status.HTTP_400_BAD_REQUEST
                    )

    @action(detail=False, methods=['get'],
            permission_classes=(permissions.IsAuthenticated, ))
    def download_shopping_cart(self, request):
        if self.request.user.is_authenticated:
            shopping_list = ShoppingCart.objects.filter(
                user=self.request.user
            ).values('recipe')
            ingredient_list = RecipeIngredients.objects.filter(
                recipe_id__in=(map(lambda x: x['recipe'], shopping_list))
            ).values('ingredient', 'amount')
            shopping_cart_dict = {}
            for item in ingredient_list:
                ingredient = Ingredient.objects.get(id=item['ingredient'])
                amount = item['amount']
                if ingredient not in shopping_cart_dict:
                    shopping_cart_dict[ingredient] = amount
                else:
                    shopping_cart_dict[ingredient] += amount
            shopping_cart = 'Список покупок: \n'
            for key in shopping_cart_dict:
                shopping_cart += f'{key} - {shopping_cart_dict[key]} \n'
            response = HttpResponse(shopping_cart, content_type='text/plain')
            response['Content-Disposition'] = (
                'attachment; filename="shopping_cart.txt"'
            )
            return response
        return Response(
                    {'detail': 'Учетные данные не были предоставлены.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
