import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from feedbacks.model_forms import FeedbackModelForm
from feedbacks.models import Feedback


@login_required
def feedbacks(request, *args, **kwargs):
    user = request.user
    form = FeedbackModelForm(request.user)
    if request.method == 'POST':
        form = FeedbackModelForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
    feedback = Feedback.objects.iterator()
    return render(request, 'feedbacks/index.html', context={
        'feedbacks': feedback,
        'form': form
    })
