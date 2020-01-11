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


class ThinReceipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Receipe
        fields = ['url', 'name', 'utensils', 'nb_people', 'stars']


class ReceipeStepReceipeSerializer(serializers.HyperlinkedModelSerializer):
    receipe_detail = ThinReceipeSerializer(source="receipe", read_only=True)


    class Meta:
        model = m.ReceipeStepReceipe
        fields = ['url', 'step', 'receipe', 'receipe_detail']


class ReceipeStepAlimentSerializer(serializers.HyperlinkedModelSerializer):
    aliment_detail = AlimentSerializer(source="aliment", read_only=True)

    class Meta:
        model = m.ReceipeStepAliment
        fields = ['url', 'step', 'aliment', 'aliment_detail', 'quantity']


class ReceipeStepSerializer(serializers.HyperlinkedModelSerializer):
    receipes = ReceipeStepReceipeSerializer(
        many=True, required=False)
    aliments = ReceipeStepAlimentSerializer(
        many=True, required=False)
    
    class Meta:
        model = m.ReceipeStep
        fields = ['url', 'receipe', 'order', 'description',
                  'duration', 'receipes', 'aliments']


class ReceipeSerializer(serializers.HyperlinkedModelSerializer):
    steps = ReceipeStepSerializer(many=True, required=False)

    class Meta:
        model = m.Receipe
        fields = ['url', 'name', 'utensils', 'nb_people', 'stars',
                  'steps']



class MealReceipeSerializer(serializers.HyperlinkedModelSerializer):
    receipe_detail = ReceipeSerializer(source="receipe", read_only=True)

    class Meta:
        model = m.MealReceipe
        fields = ['meal', 'receipe', 'receipe_detail']


class MealAlimentSerializer(serializers.HyperlinkedModelSerializer):
    aliment_detail = AlimentSerializer(source="aliment", read_only=True)

    class Meta:
        model = m.MealAliment
        fields = ['meal', 'aliment', 'quantity', 'aliment_detail']


class MealSerializer(serializers.HyperlinkedModelSerializer):
    aliments = MealAlimentSerializer(many=True, required=False)
    receipes = MealReceipeSerializer(many=True, required=False)

    class Meta:
        model = m.Meal
        fields = ['url', 'datetime', 'nb_people', 'aliments', 'receipes']