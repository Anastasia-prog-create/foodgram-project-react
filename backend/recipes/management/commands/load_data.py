from django.core.management.base import BaseCommand
from recipes.models import Ingredient
import csv


class Command(BaseCommand):
    """Комманда для загрузки ингредиентов из csv."""
    help = 'Load ingredients data'

    def handle(self, *args, **options):
        with open('recipes/data/ingredients.csv') as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name, measurement_unit = row
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=measurement_unit
                )
