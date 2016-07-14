from django.db import models
from django.utils import timezone


class Menu(models.Model):
    """Menu model class."""
    season = models.CharField(max_length=20, unique=True)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateField(default=timezone.now)
    expiration_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.season


class Item(models.Model):
    """Menu item model class."""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    chef = models.ForeignKey('auth.User')
    created_date = models.DateField(default=timezone.now)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient model class."""
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
