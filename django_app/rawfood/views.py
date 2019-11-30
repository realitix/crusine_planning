from django.contrib.auth.models import User, Group
from django.db import models
from functools import reduce
import operator
from rest_framework import viewsets
from rest_framework import filters

from rawfood import models as m
from rawfood import serializers as s


class FullTextSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(str(search_field))
            for search_field in search_fields
        ]

        conditions = []
        for search_term in search_terms:
            queries = [
                models.Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator.or_, queries))
        queryset = queryset.filter(reduce(operator.and_, conditions))

        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = s.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = s.GroupSerializer


class AlimentViewSet(viewsets.ModelViewSet):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
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


class MealStepViewSet(viewsets.ModelViewSet):
    queryset = m.MealStep.objects.all()
    serializer_class = s.MealStepSerializer
