import xmltodict
from os import path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from rawfood.models import Ingredient, IngredientCategory, IngredientNutrition


class Command(BaseCommand):
    help = 'Populate ingredients with CIQUAL data'

    def handle(self, *args, **options):
        CIQUAL_FOLDER = path.join(settings.BASE_DIR, 'ciqual_data')
        print(CIQUAL_FOLDER)