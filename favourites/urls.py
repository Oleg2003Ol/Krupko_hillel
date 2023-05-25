from django.contrib.auth.decorators import login_required
from django.urls import path

from favourites.views import FavouriteActionView, FavouriteProductsView

urlpatterns = [
    path('favourites/',
         login_required(FavouriteProductsView.as_view()),
         name='favourites'),
    path('favorites/<uuid:pk>/',
         login_required(FavouriteActionView.as_view()),
         name='add_or_remove_favorite'),
]
