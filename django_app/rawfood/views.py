from unidecode import unidecode
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import filters

from rawfood import models as m
from rawfood import serializers as s


class UnaccentSearchFilter(filters.SearchFilter):
    def get_search_terms(self, request):
        params = super().get_search_terms(request)
        return [unidecode(x) for x in params]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = s.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = s.GroupSerializer


class AlimentViewSet(viewsets.ModelViewSet):
    search_fields = ['name_search']
    filter_backends = (UnaccentSearchFilter,)
    queryset = m.Aliment.objects.all()
    serializer_class = s.AlimentSerializer


class UnitViewSet(viewsets.ModelViewSet):
    queryset = m.Unit.objects.all()
    serializer_class = s.UnitSerializer


class UtensilViewSet(viewsets.ModelViewSet):
    queryset = m.Utensil.objects.all()
    serializer_class = s.UtensilSerializer


class ReceipeViewSet(viewsets.ModelViewSet):
    queryset = m.Receipe.objects.all()
    serializer_class = s.ReceipeSerializer


class ReceipeStepReceipeViewSet(viewsets.ModelViewSet):
    queryset = m.ReceipeStepReceipe.objects.all()
    serializer_class = s.ReceipeStepReceipeSerializer


class ReceipeStepAlimentViewSet(viewsets.ModelViewSet):
    queryset = m.ReceipeStepAliment.objects.all()
    serializer_class = s.ReceipeStepAlimentSerializer


class ReceipeStepViewSet(viewsets.ModelViewSet):
    queryset = m.ReceipeStep.objects.all()
    serializer_class = s.ReceipeStepSerializer


class MealViewSet(viewsets.ModelViewSet):
    queryset = m.Meal.objects.all()
    serializer_class = s.MealSerializer


class MealReceipeViewSet(viewsets.ModelViewSet):
    queryset = m.MealReceipe.objects.all()
    serializer_class = s.MealReceipeSerializer


class MealAlimentViewSet(viewsets.ModelViewSet):
    queryset = m.MealAliment.objects.all()
    serializer_class = s.MealAlimentSerializer
