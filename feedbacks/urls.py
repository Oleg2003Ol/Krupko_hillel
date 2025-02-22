from django.urls import path

from feedbacks.views import FeedbackView, FeedbackList

urlpatterns = [
    path('create/', FeedbackView.as_view(), name='feedbacks_create'),
    path('', FeedbackList.as_view(), name='feedbacks'),
]
