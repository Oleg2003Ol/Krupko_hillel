from os import path

from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import DetailView

from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from project.model_choices import Currencies


def upload_to(instance, filename):
    _name, extension = path.splitext(filename)
    return f'products/images/{str(instance.pk)}{extension}'


class Category(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    image = models.ImageField(upload_to=upload_to,
                              null=True,
                              blank=True)

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="64" height="64"')
        else:
            return mark_safe('<b>NO IMAGE</b>')

    get_image.short_description = "Image"


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
    categories = models.ManyToManyField(Category, blank=True, unique=False)
    favorites = models.BooleanField(default=False)
    products = models.ManyToManyField("products.Product", blank=True)
    price = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES)
    currency = models.CharField(
        max_length=16,
        choices=Currencies.choices,
        default=Currencies.UAH
    )

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="64" height="64"')
        else:
            return mark_safe('<b>NO IMAGE</b>')

    get_image.short_description = "Image"

