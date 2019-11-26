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
        model = m.Aliment
        fields = ['url', 'name']


class UnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Unit
        fields = ['url', 'name']


class UtensilSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Utensil
        fields = ['url', 'name']


class ReceipeStepReceipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.ReceipeStepReceipe
        fields = ['url', 'step', 'receipe']


class ReceipeStepAlimentSerializer(serializers.HyperlinkedModelSerializer):
    aliment = AlimentSerializer()

    class Meta:
        model = m.ReceipeStepAliment
        fields = ['url', 'step', 'aliment', 'quantity', 'unit']


class ReceipeStepSerializer(serializers.HyperlinkedModelSerializer):
    receipe_ingredients = ReceipeStepReceipeSerializer(
        many=True, required=False)
    aliment_ingredients = ReceipeStepAlimentSerializer(
        many=True, required=False)
    
    class Meta:
        model = m.ReceipeStep
        fields = ['url', 'receipe', 'order', 'description',
                  'duration', 'receipe_ingredients', 'aliment_ingredients']


class ReceipeSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    steps = ReceipeStepSerializer(many=True, required=False)

    class Meta:
        model = m.Receipe
        fields = ['url', 'name', 'user', 'utensils', 'nb_people', 'stars',
                  'steps']


ReceipeStepReceipeSerializer.receipe = ReceipeSerializer()


class MealSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Meal
        fields = ['url', 'datetime', 'nb_people']


class MealStepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.MealStep
        fields = ['url', 'meal', 'name', 'ingredient']
