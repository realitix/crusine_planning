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


class ReceipeStep(models.Model):
    receipe = models.ForeignKey(Receipe, models.CASCADE, related_name="steps")
    previous_step = models.ForeignKey(
        'self', models.CASCADE, null=True, blank=True)
    description = models.TextField()
    duration = models.DurationField()

    def __str__(self):
        return self.description


class ReceipeStepReceipe(models.Model):
    step = models.ForeignKey(
        ReceipeStep, on_delete=models.CASCADE, 
        related_name="receipe_ingredients")
    receipe = models.ForeignKey(Receipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.receipe.__str__()


class ReceipeStepAliment(models.Model):
    step = models.ForeignKey(
        ReceipeStep, on_delete=models.CASCADE, 
        related_name="aliment_ingredients")
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit = models.SmallIntegerField(choices=[
        (1, "g"),
        (2, "unit")
    ])

    def __str__(self):
        return "{} {}{}".format(self.aliment, self.quantity, self.unit)


class Meal(models.Model):
    datetime = models.DateTimeField()
    nb_people = models.SmallIntegerField()

    def __str__(self):
        return self.datetime.__str__()


class MealStep(models.Model):
    meal = models.ForeignKey(Meal, models.CASCADE)
    name = models.CharField(max_length=30)
    #ingredient = models.ForeignKey(Ingredient, models.CASCADE)

    def __str__(self):
        return self.name
