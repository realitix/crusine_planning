import xmltodict
from os import path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from rawfood.models import Ingredient, IngredientCategory, IngredientNutrition


class Command(BaseCommand):
    help = 'Populate ingredients with CIQUAL data'

    def handle(self, *args, **options):
        CIQUAL_FOLDER = path.join(settings.BASE_DIR, 'ciqual_data')

        mapping_file = {
            # Contains the list of all aliments with group id
            'aliment': 'alim_2017_11_21.xml',
            # Contains all the groups and sub groups
            'group': 'alim_grp_2017_11_21.xml',
            # Contains nutrition information with aliment id and constant id
            'composition': 'compo_2017_11_21.xml',
            # Containe all the constant used in composition
            'constant': 'const_2017_11_21.xml'
        }

        ciqual_out = {}

        print("- Loading files...")
        for key, value in mapping_file.items():
            with open(path.join(CIQUAL_FOLDER, value), 'rb') as f:
                r = f.read()
                ciqual_out[key] = xmltodict.parse(r)
        print("- File loaded")
