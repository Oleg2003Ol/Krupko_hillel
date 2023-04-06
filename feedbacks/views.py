import re

from django.shortcuts import render

from feedbacks.model_forms import FeedbackModelForm
from feedbacks.models import Feedback


def feedbacks(request):
    form = FeedbackModelForm(request.user)
    if request.method == 'POST':
        form = FeedbackModelForm(user=request.user, data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.text = re.sub(r'[^\w\s]', '', review.text)
            review.text = re.sub(r'<.*?>', '', review.text)
            review.user = request.user
            review.save()
    feedback = Feedback.objects.iterator()
    return render(request, 'feedbacks/index.html', context={
        'feedbacks': feedback,
        'form': form
    })

