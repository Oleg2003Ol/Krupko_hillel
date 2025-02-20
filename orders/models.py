from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django_lifecycle import hook, AFTER_SAVE, LifecycleModelMixin, \
    AFTER_UPDATE

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
    valid_until = models.DateTimeField(
        null=True,
        blank=True
    )

    @property
    def is_valid(self):
        is_valid = self.is_active
        if self.valid_until:
            is_valid &= timezone.now() <= self.valid_until
        return is_valid


class Order(LifecycleModelMixin, PKMixin):
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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'],
                                    condition=models.Q(is_active=True),
                                    name='unique_is_active')]

    @property
    def is_current_order(self):
        return self.is_active and not self.is_paid

    def get_total_amount(self):
        total_amount = 0
        for item in self.order_items.iterator():
            total_amount += item.price * item.quantity
        if self.discount:
            if self.discount.discount_type == DiscountTypes.PERCENT:
                total_amount -= (total_amount * (self.discount.amount / 100))
            else:
                total_amount -= self.discount.amount
        return total_amount

    @hook(AFTER_UPDATE, when='discount', has_changed=True)
    def set_total_amount(self):
        self.total_amount = self.get_total_amount()
        self.save(update_fields=('total_amount',), skip_hooks=True)


class OrderItem(LifecycleModelMixin, PKMixin):
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items"
    )
    is_active = models.BooleanField(default=True)
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name="order_items"
    )
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )

    class Meta:
        unique_together = ('order', 'product')

    @property
    def sub_total(self):
        return self.price * self.quantity

    @hook(AFTER_SAVE)
    def set_order_total_amount(self):
        self.order.total_amount = self.order.get_total_amount()
        self.order.save(update_fields=('total_amount',), skip_hooks=True)
