from django.urls import path

from main.views import MainView, ContactFormView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('contact/', ContactFormView.as_view(), name='contact_form'),
]
