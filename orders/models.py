from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from project.model_choices import DiscountTypes

User = get_user_model()


class Discount(models.Model):
    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2)
    code = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    discount_type = models.PositiveSmallIntegerField(
        choices=DiscountTypes.choices,
        default=DiscountTypes.VALUE
    )


class Order(PKMixin):
    total_amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order_number = models.PositiveIntegerField(default=1)


class OrderItem(PKMixin):
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    product = models.ForeignKey(
        ...
    )
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES)
