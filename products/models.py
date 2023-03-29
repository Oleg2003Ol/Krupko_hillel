from os import path
import uuid

from django.db import models


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


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    sku = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(
        max_digits=18,
        decimal_places=2)


class Discount(models.Model):
    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2)
    code = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    discount_type = models.CharField(max_length=255,
                                     choices=((0, 'В деньгах'),
                                              (1, 'Проценты')))
