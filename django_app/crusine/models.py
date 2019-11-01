from django.db import models


class Ingredient(models.Model):
    name = models.CharField(unique=True)


class Unit(models.Model):
    name = models.CharField(unique=True)


class Utensil(models.Models):
    name = models.CharField(unique=True)


class Receipe(models.Model):
    name = models.CharField(unique=True)
    utensils = models.ManyToManyField(Utensil)
    nb_people = models.SmallIntegerField()
    stars = models.SmallIntegerField(choices=[
        (1, "very bad"),
        (2, "bad"),
        (3, 'mediocre'),
        (4, 'good'),
        (5, 'very good')
    ])


# This class allows to abstract the behavior of selecting an ingredient
# or a receipe.
# If ingredient is not null, unit and quantity must be setted and receipe must be null
class ReceipeEntry(models.Model):
    ingredient = models.ForeignKey(Ingredient)
    unit = models.ForeignKey(Unit)
    quantity = models.IntegerField()
    receipe = models.ForeignKey(Receipe)


class ReceipeStep(models.Model):
    receipe = models.ForeignKey(Receipe)
    previous_step = models.ForeignKey('self')
    description = models.TextField()
    duration = models.DurationField()


# Receipe can contain ingredient
class ReceipeStepEntry(models.Model):
    receipe_step = models.ForeignKey(ReceipeStep)
    receipe_entry = models.ForeignKey(ReceipeEntry)


class Meal(models.Model):
    datetime = models.DateTimeField()
    nb_people = models.SmallIntegerField()


class MealStep(models.Model):
    meal = models.ForeignKey(Meal)
    name = models.CharField()
    receipe_entry = models.ForeignKey(Receipe)