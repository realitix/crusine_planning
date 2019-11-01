from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from crusine import models as m
from crusine import serializers as s


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
