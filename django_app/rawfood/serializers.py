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


class AlimentSerializer(serializers.HyperlinkedModelSerializer):
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
    steps = serializers.RelatedField(
        many=True, required=False, queryset=m.ReceipeStep.objects.all())

    class Meta:
        model = m.Receipe
        fields = ['url', 'name', 'user', 'utensils', 'nb_people', 'stars',
                  'steps']


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Ingredient
        fields = ['url', 'receipe', 'aliment', 'unit', 'quantity']


class ReceipeStepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.ReceipeStep
        fields = ['url', 'receipe', 'previous_step', 'description', 'duration']


class MealSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Meal
        fields = ['url', 'datetime', 'nb_people']


class MealStepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.MealStep
        fields = ['url', 'meal', 'name', 'ingredient']
