from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

from rawfood import models as m
from rawfood import serializers as s


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = s.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = s.GroupSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = m.Ingredient.objects.all()
    serializer_class = s.IngredientSerializer


class UnitViewSet(viewsets.ModelViewSet):
    queryset = m.Unit.objects.all()
    serializer_class = s.UnitSerializer


class UtensilViewSet(viewsets.ModelViewSet):
    queryset = m.Utensil.objects.all()
    serializer_class = s.UtensilSerializer


class ReceipeViewSet(viewsets.ModelViewSet):
    queryset = m.Receipe.objects.all()
    serializer_class = s.ReceipeSerializer


class ReceipeEntryViewSet(viewsets.ModelViewSet):
    queryset = m.ReceipeEntry.objects.all()
    serializer_class = s.ReceipeEntrySerializer


class ReceipeStepViewSet(viewsets.ModelViewSet):
    queryset = m.ReceipeStep.objects.all()
    serializer_class = s.ReceipeStepSerializer


class ReceipeStepEntryViewSet(viewsets.ModelViewSet):
    queryset = m.ReceipeStepEntry.objects.all()
    serializer_class = s.ReceipeStepEntrySerializer


class MealViewSet(viewsets.ModelViewSet):
    queryset = m.Meal.objects.all()
    serializer_class = s.MealSerializer


class MealStepViewSet(viewsets.ModelViewSet):
    queryset = m.MealStep.objects.all()
    serializer_class = s.MealStepSerializer
