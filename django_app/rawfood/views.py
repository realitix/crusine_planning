from unidecode import unidecode
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import filters
from django_filters import rest_framework as djfilters
from rest_framework.decorators import action
import django_filters
from django.db import models as django_models
from rest_framework.response import Response
import datetime

from rawfood import models as m
from rawfood import serializers as s


class UnaccentSearchFilter(filters.SearchFilter):
    def get_search_terms(self, request):
        params = super().get_search_terms(request)
        return [unidecode(x) for x in params]


class MealDatetimeFilter(djfilters.FilterSet):
    class Meta:
        model = m.Meal
        fields = {
            'datetime': ('lte', 'gte')
        }

    filter_overrides = {
        django_models.DateTimeField: {
            'filter_class': django_filters.IsoDateTimeFilter
        },
    }


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
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
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
    filter_backends = (djfilters.DjangoFilterBackend, )
    filter_class = MealDatetimeFilter

    @action(detail=False)
    def next_preparation(self, request):
        # Display receipe from this algorythm:
        # We remove the time from selected datetime
        # We remove one day more to be sure to not forget something more
        get_date = request.GET.get('datetime')
        current_date = datetime.datetime.fromtimestamp(get_date)
        meals = m.Meal.objects.all()
        serializer = self.get_serializer(meals, many=True)
        return Response(serializer.data)


class MealReceipeViewSet(viewsets.ModelViewSet):
    queryset = m.MealReceipe.objects.all()
    serializer_class = s.MealReceipeSerializer


class MealAlimentViewSet(viewsets.ModelViewSet):
    queryset = m.MealAliment.objects.all()
    serializer_class = s.MealAlimentSerializer
