from django.contrib.auth.models import User, Group
from rest_framework import serializers

from rawfood import models as m


class UserSerializer(serializers.HyperlinkedModelSerializer):
    receipes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=m.Receipe.objects.all())

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'receipes']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Ingredient
        fields = ['url', 'name']


class UnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Unit
        fields = ['url', 'name']


class UtensilSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Utensil
        fields = ['url', 'name']


class ReceipeSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = m.Receipe
        fields = ['url', 'name', 'user', 'utensils', 'nb_people', 'stars']


class ReceipeEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.ReceipeEntry
        fields = ['url', 'receipe', 'ingredient', 'unit', 'quantity']


class ReceipeStepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.ReceipeStep
        fields = ['url', 'receipe', 'previous_step', 'description', 'duration']


class ReceipeStepEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.ReceipeStepEntry
        fields = ['url', 'receipe_step', 'receipe_entry']


class MealSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Meal
        fields = ['url', 'datetime', 'nb_people']


class MealStepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.MealStep
        fields = ['url', 'meal', 'name', 'receipe_entry']
