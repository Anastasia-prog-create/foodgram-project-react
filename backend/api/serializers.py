from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, validators
from recipes.models import (FavoriteList, Ingredient, Recipe,
                            RecipeIngredients, ShoppingCart, Tag)
from users.models import Subscribe, User


class UserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания модели User."""
    username = serializers.RegexField(
        required=True,
        regex=r'^[\w.@+-]+',
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password'
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра моделей User."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        lookup_field = (
            'username',
            'email'
        )

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_authenticated:
            return Subscribe.objects.filter(
                user=obj, subscriber=self.context['request'].user
            ).exists()
        return False


class PasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля."""
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания подписки."""

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    subscriber = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Subscribe
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=['user', 'subscriber'],
                message='Такая подписка уже существует.'
            )
        ]

    def validate_user(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError('Подписка на себя невозможна.')
        return value


class TagSerializer(serializers.ModelSerializer):
    '''Сериализатор для просмотра тэгов.'''

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    '''Сериализатор для просмотра ингредиентов.'''

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientsSerializer(serializers.ModelSerializer):
    '''Сериализатор для добавления ингредиентов в рецепт.'''
    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredients
        fields = (
            'id',
            'amount',
        )


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    '''Сериализатор просмотра ингредиентов в рецепте.'''
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    measurement_unit = serializers.IntegerField(read_only=True)
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = RecipeIngredients
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецептов."""
    ingredients = IngredientsSerializer(
        many=True,
        source='recipeingredients_set',
        required=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True
    )
    image = Base64ImageField(
        required=True,
        represent_in_base64=True
    )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('recipeingredients_set')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            amount = ingredient.get('amount')
            RecipeIngredients.objects.create(
                ingredient=get_object_or_404(
                    Ingredient, pk=ingredient.get('id')
                ),
                amount=amount,
                recipe=recipe
            )
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipeingredients_set')
        tags = validated_data.pop('tags')

        recipe = super().update(instance, validated_data)
        instance.tags.set = recipe.tags.set(tags)
        for ingredient in ingredients:
            amount = ingredient.get('amount')
            RecipeIngredients.objects.get_or_create(
                ingredient=get_object_or_404(
                    Ingredient, pk=ingredient.get('id')
                ),
                amount=amount,
                recipe=recipe
            )
        return recipe


class RecipeGETSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра рецептов."""
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientsSerializer(
        many=True,
        source='recipeingredients_set',
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        return (
            self.context['request'].user.is_authenticated
            and FavoriteList.objects.filter(
                recipe=obj, user=self.context['request'].user
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        return (
            self.context['request'].user.is_authenticated
            and ShoppingCart.objects.filter(
                recipe=obj, user=self.context['request'].user
            ).exists()
        )


class FavoriteANDShoppingListSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецептов в избранное/корзину."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscribesListSerializer(UserSerializer):
    """Сериализатор для вывода списка подписок."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        if self.context['request'].query_params.get('recipes_limit'):
            limit = int(self.context['request'].query_params.get(
                'recipes_limit')
            )
            recipes = Recipe.objects.filter(author=obj)[:limit]
        else:
            recipes = Recipe.objects.filter(author=obj)
        serializer = RecipeGETSerializer(
            recipes,
            many=True,
            context={'request': self.context['request']}
        )
        return serializer.data
