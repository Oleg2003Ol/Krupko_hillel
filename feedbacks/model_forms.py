from django import forms

from feedbacks.models import Feedback


class FeedbackModelForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Feedback
        fields = ['text', 'rating']
