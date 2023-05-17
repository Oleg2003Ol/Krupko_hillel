from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django import forms

from feedbacks.models import Feedback


class FeedbackModelForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].initial = user

    class Meta:
        model = Feedback
        fields = ('text', 'user', 'rating')

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
            raise ValidationError('This field is required.')
        clean_text = strip_tags(text)
        return clean_text

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)

    def save(self, commit=True, user=None, request=None):
        feedback = super().save(commit=False)
        if user:
            feedback.user = user
        if commit:
            feedback.save()
        messages.success(request, 'Feedback posted!')
        return feedback
