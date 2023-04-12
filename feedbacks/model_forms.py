from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django import forms

from feedbacks.models import Feedback


class FeedbackModelForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Feedback
        fields = ['text', 'rating']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
            raise ValidationError('This field is required.')
        clean_text = strip_tags(text)
        return clean_text
