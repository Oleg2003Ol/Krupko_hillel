from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_lifecycle import hook, AFTER_CREATE, \
    AFTER_UPDATE, LifecycleModelMixin

from project.mixins.models import PKMixin
from project.model_choices import FeedbackCacheKeys


class Feedback(LifecycleModelMixin, PKMixin):
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

    @hook(AFTER_CREATE)
    @hook(AFTER_UPDATE)
    def after_update_feedback_signal(self):
        cache.delete(FeedbackCacheKeys.FEEDBACKS)
