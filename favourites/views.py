from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from favourites.models import FavouriteProduct
from products.models import Product


class FavouriteProductsView(ListView):
    model = FavouriteProduct

    def get_queryset(self):
        return FavouriteProduct.objects.select_related('product', 'user') \
            .prefetch_related('product__products')


class FavouriteActionView(DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        favorite, created = FavouriteProduct.objects.get_or_create(
            product=product,
            user=user
        )
        if created:
            messages.success(request, 'Product add to Favorites!')
        if not created:
            favorite.delete()
            messages.success(request, 'Product delete from Favorites!')
        return HttpResponseRedirect(reverse_lazy('products'))
