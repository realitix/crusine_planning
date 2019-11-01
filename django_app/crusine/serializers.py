from django.contrib.auth.models import User, Group
from rest_framework import serializers

from crusine.models import Ingredient, Unit, Utensil


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
        model = Ingredient
        fields = ['name']


class UnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Unit
        fields = ['name']


class UtensilSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Utensil
        fields = ['name']
