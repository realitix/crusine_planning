import urllib.request
import unidecode
import json
from os import path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from rawfood.models import Aliment, AlimentCategory, AlimentNutrition


class Command(BaseCommand):
    help = 'Populate ingredients with Food data'
    url = "https://raw.githubusercontent.com/realitix/food-database/master/out/data.json"

    def download_data():
        response = urllib.request.urlopen(Command.url)
        data = json.loads(response.read())
        return data

    def populate_database(data):
        # Insert group
        group_mapping = {}
        for x in data:
            gname = x['group_name_fr']
            gfresh = x['fresh']
            if gname in group_mapping:
                continue

            try:
                cat = AlimentCategory.objects.get(name=gname)
            except AlimentCategory.DoesNotExist:
                cat = AlimentCategory(name=gname, fresh=gfresh)
                cat.save()

            group_mapping[gname] = cat

        # Insert aliment
        for x in data:
            cat = group_mapping[x['group_name_fr']]
            n = x['name_fr']
            s = unidecode.unidecode(n)

            try:
                ingredient = Aliment.objects.get(name=n)
                if ingredient.name_search != s:
                    ingredient.name_search = s
                    ingredient.save()
                continue
            except Aliment.DoesNotExist:
                ingredient = Aliment(name=n, name_search=s, category=cat)
                ingredient.save()

            n = x['nutrition']
            nutrition = AlimentNutrition(
                aliment=ingredient, protein=n['protein'],
                glucid=n['glucid'], lipid=n['lipid'])
            nutrition.save()

    def handle(self, *args, **options):
        # Load data
        print('- Download data... ', end='', flush=True)
        data = Command.download_data()
        print('OK')

        # Insert data in database
        print('- Populate database... ', end='', flush=True)
        Command.populate_database(data['aliments'])
        print('OK')

        print('-- Generation finished --')
