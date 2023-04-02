from os import path

from django.db import models
from django.core.validators import MinValueValidator
from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin


def upload_to(instance, filename):
    _name, extension = path.splitext(filename)
    return f'products/images/{str(instance.pk)}{extension}'


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    image = models.ImageField(upload_to=upload_to,
                              null=True,
                              blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    image = models.ImageField(upload_to=upload_to,
                              null=True,
                              blank=True)
    sku = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True)
    products = models.ManyToManyField("products.Product", blank=True)
    price = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES)

    def __str__(self):
        return f"{self.image} {self.name}"


class Discount(models.Model):
    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2)
    code = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    discount_type = models.CharField(max_length=255,
                                     choices=((0, 'В деньгах'),
                                              (1, 'Проценты')))
    # поменять на SmallInteger
