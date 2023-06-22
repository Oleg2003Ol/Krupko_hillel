from django.contrib.auth.decorators import login_required
from django.urls import path

from favourites.views import FavouriteActionView, FavouriteProductsView, \
    AJAXAddOrRemoveFavoriteProduct

urlpatterns = [
    path('favourites/',
         login_required(FavouriteProductsView.as_view()),
         name='favourites'),
    path('favourite/<uuid:pk>/',
         login_required(FavouriteActionView.as_view()),
         name='add_or_remove_favourite'),
    path('ajax-favourite/<uuid:pk>/', AJAXAddOrRemoveFavoriteProduct.as_view(),
         name='ajax_add_or_remove_favourite'),
]
