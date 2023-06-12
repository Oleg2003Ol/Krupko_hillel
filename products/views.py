import csv

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, DetailView
from django.http import HttpResponse, Http404
from django.views import View
from django.core.paginator import Paginator
from django_filters.views import FilterView

from .filters import ProductFilter
from .forms import ImportCSVForm
from .models import Product, Category
from .tasks import parse_products
from project.model_choices import ProductCacheKeys


class ProductsListView(FilterView):
    model = Product
    template_name = 'products/index.html'
    context_object_name = 'products'
    paginate_by = 8
    filterset_class = ProductFilter

    def get_queryset(self):
        return (
            Product.objects.prefetch_related(
                Prefetch('categories', queryset=Category.objects.only('name')),
                Prefetch('products', queryset=Product.objects.only('name'))
            )
            .all()
        )

    # def get(self, request, *args, **kwargs):
    #     parse_products()
    #     return super().get(request=request, *args, **kwargs)


class ProductDetail(DetailView):
    context_object_name = 'product'
    model = Product

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            # Get the single item from the filtered queryset
            obj = cache.get_or_set(f"{ProductCacheKeys.PRODUCTS}_{pk}",
                                   queryset.get())
        except queryset.model.DoesNotExist:
            raise Http404(
                "No %(verbose_name)s found matching the query"
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj

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
