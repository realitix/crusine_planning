from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from crusine.models import Ingredient, Unit, Utensil
from crusine import serializers as s


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = s.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = s.GroupSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = s.IngredientSerializer


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = s.UnitSerializer


class UtensilViewSet(viewsets.ModelViewSet):
    queryset = Utensil.objects.all()
    serializer_class = s.UtensilSerializer
