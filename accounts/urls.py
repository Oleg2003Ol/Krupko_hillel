from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import RegistrationView, LoginView, \
    ProfileListView, VerificationPhoneView

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileListView.as_view(), name='profile'),
    path('verification-phone/', VerificationPhoneView.as_view(),
         name='verify_phone')
]
