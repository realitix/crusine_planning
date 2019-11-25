import xmltodict
import re
from os import path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from rawfood.models import Aliment, AlimentCategory, AlimentNutrition


class Command(BaseCommand):
    help = 'Populate ingredients with CIQUAL data'

    def load_files():
        CIQUAL_FOLDER = path.join(settings.BASE_DIR, 'ciqual_data')

        filenames = [
            # Contains the list of all aliments with group id
            'alim_2017_11_21.xml',
            # Contains all the groups and sub groups
            'alim_grp_2017_11_21.xml',
            # Contains nutrition information with aliment id and constant id
            'compo_2017_11_21.xml',
            # Containe all the constant used in composition
            'const_2017_11_21.xml'
        ]

        ciqual_out = {}

        for filename in filenames:
            with open(path.join(CIQUAL_FOLDER, filename), 'rb') as f:
                r = f.read()
                ciqual_out.update(xmltodict.parse(r)['TABLE'])

        return ciqual_out

    def format_data(data_raw):
        # ALIM []:
        # alim_code, alim_nom_fr, alim_nom_index_fr, alim_grp_code
        # alim_ssgrp_code, alim_ssssgrp_code
        #
        # ALIM_GRP []:
        # alim_grp_code, alim_grp_nom_fr, alim_ssgrp_code,
        # alim_ssgrp_nom_fr, alim_ssssgrp_code, alim_ssssgrp_nom_fr
        #
        # COMPO []:
        # alim_code, const_code, teneur, min, max, code_confiance,
        # source_code
        #
        # CONST []:
        # const_code, const_nom_fr

        groups = {
            '0000': '-'
        }
        for g in data_raw['ALIM_GRP']:
            groups[g['alim_grp_code']] = g['alim_grp_nom_fr']
            groups[g['alim_ssgrp_code']] = g['alim_ssgrp_nom_fr']
            groups[g['alim_ssssgrp_code']] = g['alim_ssssgrp_nom_fr']

        # Name in xml to column name in database
        # The second element in the tuple is the multiplicator
        # All in microgram
        mapping_nutrition = {
            'Protéines (g/100g)': ('protein', 10000),
            'Glucides (g/100g)': ('glucid', 10000),
            'Lipides (g/100g)': ('lipid', 10000)
        }

        mapping_constant = {}
        for x in data_raw['CONST']:
            cn = x['const_nom_fr']
            if cn in mapping_nutrition:
                mapping_constant[x['const_code']] = mapping_nutrition[cn]
        
        data = []
        for a in data_raw['ALIM']:
            code_ciqual = a['alim_code']

            if groups[a['alim_ssssgrp_code']] != '-':
                group_name = groups[a['alim_ssssgrp_code']]
            elif groups[a['alim_ssgrp_code']] != '-':
                group_name = groups[a['alim_ssgrp_code']]
            else:
                group_name = groups[a['alim_grp_code']]

            nutrition = {}
            for x in data_raw['COMPO']:
                if x['alim_code'] == code_ciqual:
                    if x['const_code'] not in mapping_constant:
                        continue

                    val = x['teneur']
                    if val == '-':
                        val = ''
                    
                    # remove non decimal char
                    val = re.sub(r'[^\d.]+', '', val)
                    if not val:
                        val = 0
                    else:
                        val = float(val.replace(',', '.'))

                    nutrition_name = mapping_constant[x['const_code']][0]
                    multilicator = mapping_constant[x['const_code']][1]

                    nutrition[nutrition_name] = int(val * multilicator)
                    
            data.append({
                'code_ciqual': code_ciqual,
                'name': a['alim_nom_fr'],
                'name2': a['alim_nom_index_fr'],
                'group_name': group_name,
                'nutrition': nutrition
            })
        
        return data

    def filter_data(data):
        # groups classified fresh
        fresh_group = [
            'fruits crus',
            'herbes fraîches',
            'légumes cuits',
            'légumes crus',
            'poissons crus',
        ]

        # Keep only selected group
        accepted_group = [
            'fruits crus',
            'herbes fraîches',
            'légumes cuits',
            'légumes crus',
            'poissons crus',
            'épices',
            'fruits à coque et graines oléagineuses',
            'huiles et graisses végétales',
            'chocolats et produits à base de chocolat',
            'beurres',
            'légumes séchés ou déshydratés',
            'fruits séchés',
            'œufs cuits',
            'herbes séchées',
            'laits autres que de vache',
            'pommes de terre et autres tubercules',
            'sels',
            'algues',
            'légumineuses fraîches',
            'pâtes, riz et céréales crus',
            'condiments',
            'sucres, miels et assimilés',
            'boissons végétales',
            'légumineuses cuites',
            'poissons cuits',
            'farines',
            'autres matières grasses',
            'poulet',
            'légumineuses sèches',
            'pâtes, riz et céréales cuits',
            'mollusques et crustacés crus',
            # 'agneau et mouton',
            # 'cocktails',
            # 'café, thé, cacao etc. prêts à consommer',
            # 'fromages à pâte persillée',
            # 'mollusques et crustacés cuits',
            # 'pizzas, tartes et crêpes salées',
            # 'laits et boissons infantiles',
            # 'viennoiseries',
            # 'gibier',
            # 'laits de vache concentrés ou en poudre',
            # 'plats de poisson et féculents',
            # 'margarines',
            # 'desserts glacés',
            # 'compotes et assimilés',
            # 'biscottes et pains grillés',
            # 'sandwichs',
            # 'salades composées et crudités',
            # 'desserts lactés',
            # 'plats de poisson sans garniture',
            # 'pains',
            # 'boissons rafraîchissantes sans alcool',
            # 'plats de viande sans garniture',
            # 'pâtes à tarte',
            # 'saucisses et assimilés',
            # 'huiles de poissons',
            # 'abats',
            # 'boissons à reconstituer',
            # 'autres fromages et spécialités',
            # 'autres desserts',
            # 'laits de vaches liquides (non concentrés)',
            # 'petits pots salés et plats infantiles',
            # 'céréales de petit-déjeuner',
            # 'plats de viande et légumes/légumineuses',
            # 'eaux',
            # 'sorbets',
            # 'autres viandes',
            # 'gâteaux et pâtisseries',
            # 'confiseries non chocolatées',
            # 'biscuits sucrés',
            # 'jambons cuits',
            # 'porc',
            # 'quenelles',
            # 'saucisson secs',
            # 'céréales et biscuits infantiles',
            # 'jus',
            # 'nectars',
            # 'sauces sucrées',
            # 'crèmes et spécialités à base de crème',
            # 'soupes',
            # 'desserts infantiles',
            # 'autres spécialités charcutières',
            # 'confitures et assimilés',
            # 'denrées destinées à une alimentation particulière',
            # 'plats de fromage',
            # 'dinde',
            # 'charcuteries',
            # 'glaces',
            # 'fromages',
            # 'boissons rafraîchissantes lactées',
            # 'jambons secs et crus',
            # 'biscuits apéritifs',
            # 'aides culinaires',
            # 'rillettes',
            # 'vins',
            # 'produits à base de poissons et produits de la mer',
            # 'viandes cuites',
            # 'sauces chaudes',
            # 'plats de viande et féculents',
            # 'plats de céréales/pâtes',
            # 'fromages à pâte molle',
            # 'bières et cidres',
            # 'autres produits à base de viande',
            # 'fromages à pâte pressée',
            # 'œufs crus',
            # 'fruits appertisés',
            # 'ingrédients divers',
            # 'fromage fondus',
            # 'feuilletées et autres entrées',
            # 'pâtés et terrines',
            # 'fromages blancs',
            # 'omelettes et autres ovoproduits',
            # 'sauces condimentaires',
            # 'bœuf et veau',
            # 'barres céréalières',
            # 'glaces et sorbets'
        ]

        filtered_data = []
        for d in data:
            if d['group_name'] in accepted_group:
                d['group_fresh'] = d['group_name'] in fresh_group
                filtered_data.append(d)

        return filtered_data

    def populate_database(data):
        # Insert group
        group_mapping = {}
        for x in data:
            gname = x['group_name']
            gfresh = x['group_fresh']
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
            cat = group_mapping[x['group_name']]

            try:
                Aliment.objects.get(name=x['name'])
                continue
            except Aliment.DoesNotExist:
                ingredient = Aliment(name=x['name'], category=cat)
                ingredient.save()

            n = x['nutrition']
            nutrition = AlimentNutrition(
                aliment=ingredient, protein=n['protein'],
                glucid=n['glucid'], lipid=n['lipid'])
            nutrition.save()

    def handle(self, *args, **options):
        # Load data
        print('- Loading files... ', end='', flush=True)
        data_raw = Command.load_files()
        print('OK')

        # Reformat data
        print('- Format data... ', end='', flush=True)
        data_formatted = Command.format_data(data_raw)
        print('OK')

        # Filter data
        print('- Filter data... ', end='', flush=True)
        data_filtered = Command.filter_data(data_formatted)
        print('OK')

        # Insert data in database
        print('- Populate database... ', end='', flush=True)
        Command.populate_database(data_filtered)
        print('OK')

        print('-- Generation finished --')
