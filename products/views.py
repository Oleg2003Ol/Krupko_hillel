import csv
from django.views.generic import ListView
from .models import Product
from django.http import HttpResponse
from django.views import View
from .models import Product


class ProductsListView(ListView):
    model = Product
    template_name = 'products/index.html'
    context_object_name = 'products'


class ExportCSVView(View):
    template_name = 'products/export_to_pdf.html'

    def get(self, request, *args, **kwargs):
        headers = {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="products.csv"'
        }
        response = HttpResponse(headers=headers)
        fields_name = ['name', 'description', 'sku', 'image', 'price', 'is_active']
        writer = csv.DictWriter(response, fieldnames=fields_name, delimiter=';')
        writer.writeheader()
        for product in Product.objects.iterator():
            writer.writerow(
                {
                    'name': product.name,
                    'description': product.description,
                    'image': product.image.name if product.image else 'no image',
                    'sku': product.sku,
                    'price': product.price,
                    'is_active': product.is_active
                }
            )
        return response
