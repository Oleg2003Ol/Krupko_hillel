from django.contrib.auth import get_user_model

from products.models import Product
from project.mixins.models import PKMixin
from django.db import models


class FavouriteProduct(PKMixin):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='favorite_products'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='in_favorites'
    )

    class Meta:
        unique_together = ('user', 'product')
