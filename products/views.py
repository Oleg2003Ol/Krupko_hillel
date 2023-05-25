import csv

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView
from django.http import HttpResponse
from django.views import View

from .forms import ImportCSVForm
from .models import Product, Category


class ProductsListView(ListView):
    model = Product
    template_name = 'products/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return (
            Product.objects.prefetch_related(
                Prefetch('categories', queryset=Category.objects.only('name')),
                Prefetch('products', queryset=Product.objects.only('name'))
            )
            .all()
        )


@method_decorator(login_required, name='dispatch')
class ExportCSVView(View):

    def get(self, request, *args, **kwargs):
        headers = {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="products.csv"'
        }
        response = HttpResponse(headers=headers)
        fields_name = ['name', 'description', 'sku', 'image',
                       'price', 'is_active', 'categories']
        writer = csv.DictWriter(response, fieldnames=fields_name)
        writer.writeheader()
        for product in Product.objects.iterator():
            categories = ", ".join(
                [category.name for category in product.categories.all()])
            writer.writerow(
                {
                    'name': product.name,
                    'description': product.description,
                    'image': product.image.name if product.image
                    else 'no image',
                    'sku': product.sku,
                    'price': product.price,
                    'is_active': product.is_active,
                    'categories': categories
                }
            )
        return response


class ProductImportCSVView(FormView):
    form_class = ImportCSVForm
    template_name = 'products/import_csv.html'
    success_url = reverse_lazy('products')

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
