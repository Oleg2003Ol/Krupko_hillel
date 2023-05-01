from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from favourites.models import FavouriteProduct
from products.models import Product


class FavouriteProductsView(ListView):
    model = FavouriteProduct

    def get_queryset(self):
        qs = FavouriteProduct.objects.select_related('product', 'user') \
            .prefetch_related('product__products')
        return qs


class FavouriteActionView(DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        favorite, created = FavouriteProduct.objects.get_or_create(
            product=product,
            user=user
        )
        if not created:
            favorite.delete()
        return HttpResponseRedirect(reverse_lazy('products'))


