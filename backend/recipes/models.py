from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    """Модель тэга."""
    name = models.TextField('Имя', unique=True)
    color = models.CharField('Цвет', max_length=7, unique=True)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Tэг'
        verbose_name_plural = 'Tэги'

    def __str__(self):
        return str(self.name)


class Ingredient(models.Model):
    """Модель ингредиента."""
    name = models.TextField('Имя')
    measurement_unit = models.TextField('Единица измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        User,
        related_name='author',
        on_delete=models.CASCADE,
    )
    name = models.CharField('Название', max_length=200)
    text = models.TextField('Описание')
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Время приготовления не может быть меньше 1 мин.'
            ),
        ]
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Список ингредиентов',
        through='RecipeIngredients',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='./media/recipes/images'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return str(self.name)


class RecipeIngredients(models.Model):
    """Модель связи рецепт-ингредиент."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Количество ингредиента не может быть меньше 1 ед.'
            ),
        ]
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Рецепт-ингредиенты'
        verbose_name_plural = 'Рецепт-ингредиенты'

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class BaseFavorite(models.Model):
    """Модель для избранного/корзины."""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class FavoriteList(BaseFavorite):

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique favorite'
            ),
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(BaseFavorite):

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique favorite'
            ),
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'
