# Generated by Django 2.2.19 on 2022-05-17 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20220509_1545'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipeingredients',
            options={'ordering': ('recipe',), 'verbose_name': 'Рецепт-ингредиенты', 'verbose_name_plural': 'Рецепт-ингредиенты'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='./media/recipes/images', verbose_name='Изображение'),
        ),
    ]
