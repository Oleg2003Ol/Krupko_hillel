from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from favourites.models import FavouriteProduct
from products.models import Product
from project.decorators import ajax_required


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


class AJAXAddOrRemoveFavoriteProduct(DetailView):
    model = Product

    @method_decorator(login_required)
    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        favourite, created = FavouriteProduct.objects.get_or_create(
            product=product,
            user=request.user
        )
        if not created:
            favourite.delete()
        return JsonResponse({'is_favourite': created})
