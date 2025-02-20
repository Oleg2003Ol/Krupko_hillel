import os

from django.db import models
from django.core.validators import MinValueValidator
from django_lifecycle import hook, BEFORE_CREATE, BEFORE_UPDATE
from slugify import slugify

from currencies.models import CurrencyHistory
from project import settings
from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from project.model_choices import Currencies


def upload_to(instance, filename):
    _name, extension = os.path.splitext(filename)
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
    is_manual_slug = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when='name', has_changed=True)
    def after_signal(self):
        if not self.is_manual_slug:
            self.slug = slugify(self.name)


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

    @property
    def price_uah(self):
        latest_rate = CurrencyHistory.objects.filter(
            code=self.currency
        ).order_by('-created_at').first()
        if not latest_rate:
            return self.price
        return self.price * latest_rate.sale

    @hook(BEFORE_UPDATE, when='image')
    def after_update_signal(self):
        if self.initial_value('image'):
            image_path = os.path.join(settings.BASE_DIR,
                                      settings.MEDIA_ROOT,
                                      str(self.initial_value('image')))
            try:
                os.remove(image_path)
            except (FileNotFoundError, OSError, IOError):
                ...

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
