from django.contrib.auth.models import User, Group
from rest_framework import serializers

from crusine import models as m


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Ingredient
        fields = ['name']


class UnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Unit
        fields = ['name']


class UtensilSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Utensil
        fields = ['name']


class ReceipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Receipe
        fields = ['name', 'utensils', 'nb_people', 'stars']


class ReceipeEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.ReceipeEntry
        fields = ['receipe', 'ingredient', 'unit', 'quantity']


class ReceipeStepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.ReceipeStep
        fields = ['receipe', 'previous_step', 'description', 'duration']


class ReceipeStepEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.ReceipeStepEntry
        fields = ['receipe_step', 'receipe_entry']


class MealSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Meal
        fields = ['datetime', 'nb_people']
