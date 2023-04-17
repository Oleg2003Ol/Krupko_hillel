from django.urls import reverse
from django.views.generic import ListView
from .models import Product


class ProductsListView(ListView):
    model = Product
    template_name = 'products/index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_url'] = reverse('products')
        return context
