from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class AlimentCategory(models.Model):
    name = models.CharField(unique=True, max_length=50)
    fresh = models.BooleanField()

    def __str__(self):
        return self.name


class Aliment(models.Model):
    name = models.CharField(unique=True, max_length=50)
    category = models.ForeignKey(
        AlimentCategory,
        on_delete=models.CASCADE,
        related_name="aliments"
    )

    def __str__(self):
        return self.name


class AlimentNutrition(models.Model):
    # All fields are in microgram
    protein = models.PositiveIntegerField()
    glucid = models.PositiveIntegerField()
    lipid = models.PositiveIntegerField()

    aliment = models.OneToOneField(
        Aliment,
        on_delete=models.CASCADE,
        primary_key=True
    )

    def __str__(self):
        return "Nutrition " + self.ingredient.name


class Unit(models.Model):
    name = models.CharField(unique=True, max_length=30)

    def __str__(self):
        return self.name


class Utensil(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Receipe(models.Model):
    name = models.CharField(unique=True, max_length=150)
    user = models.ForeignKey(
        'auth.User', related_name="receipes",
        on_delete=models.CASCADE)
    utensils = models.ManyToManyField(
        Utensil, related_name="receipes", blank=True)
    nb_people = models.SmallIntegerField(blank=True, default=1)
    stars = models.SmallIntegerField(choices=[
        (1, "very bad"),
        (2, "bad"),
        (3, 'mediocre'),
        (4, 'good'),
        (5, 'very good')
    ], blank=True, default=3)

    def __str__(self):
        return self.name


# This class allows to abstract the behavior of selecting an ingredient
# or a receipe.
# If ingredient is not null, unit and quantity must be setted and receipe
# must be null
class Ingredient(models.Model):
    receipe = models.ForeignKey(
        Receipe, on_delete=models.CASCADE, blank=True, null=True)
    aliment = models.ForeignKey(
        Aliment, on_delete=models.CASCADE, blank=True, null=True)
    unit = models.ForeignKey(
        Unit, models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.receipe:
            return self.receipe.__str__()
        return "{} {}{}".format(self.aliment, self.quantity, self.unit)


class ReceipeStep(models.Model):
    receipe = models.ForeignKey(Receipe, models.CASCADE, related_name="steps")
    previous_step = models.ForeignKey(
        'self', models.CASCADE, null=True, blank=True)
    description = models.TextField()
    duration = models.DurationField()
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.description


class Meal(models.Model):
    datetime = models.DateTimeField()
    nb_people = models.SmallIntegerField()

    def __str__(self):
        return self.datetime.__str__()


class MealStep(models.Model):
    meal = models.ForeignKey(Meal, models.CASCADE)
    name = models.CharField(max_length=30)
    ingredient = models.ForeignKey(Ingredient, models.CASCADE)

    def __str__(self):
        return self.name
