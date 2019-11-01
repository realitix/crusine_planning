from django.db import models


class Ingredient(models.Model):
    name = models.CharField(unique=True, max_length=50)


class Unit(models.Model):
    name = models.CharField(unique=True, max_length=30)


class Utensil(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Receipe(models.Model):
    name = models.CharField(unique=True, max_length=150)
    utensils = models.ManyToManyField(Utensil, related_name="receipes")
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
# If ingredient is not null, unit and quantity must be setted and receipe
# must be null
class ReceipeEntry(models.Model):
    receipe = models.ForeignKey(
        Receipe, on_delete=models.CASCADE, blank=True, null=True)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, blank=True, null=True)
    unit = models.ForeignKey(
        Unit, models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)


class ReceipeStep(models.Model):
    receipe = models.ForeignKey(Receipe, models.CASCADE)
    previous_step = models.ForeignKey('self', models.CASCADE)
    description = models.TextField()
    duration = models.DurationField()


# Receipe can contain ingredient
class ReceipeStepEntry(models.Model):
    receipe_step = models.ForeignKey(ReceipeStep, models.CASCADE)
    receipe_entry = models.ForeignKey(ReceipeEntry, models.CASCADE)


class Meal(models.Model):
    datetime = models.DateTimeField()
    nb_people = models.SmallIntegerField()


class MealStep(models.Model):
    meal = models.ForeignKey(Meal, models.CASCADE)
    name = models.CharField(max_length=30)
    receipe_entry = models.ForeignKey(Receipe, models.CASCADE)
