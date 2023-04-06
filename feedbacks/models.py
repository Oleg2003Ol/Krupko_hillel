from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from project.mixins.models import PKMixin


class Feedback(PKMixin):
    objects = None
    text = models.TextField()
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(5),)
    )

    def __str__(self):
        return f"{self.text} - {self.rating}"
