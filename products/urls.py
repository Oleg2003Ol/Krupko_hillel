from django.urls import path

from .views import ProductsListView, ExportCSVView, ProductImportCSVView, ProductDetail

urlpatterns = [
    path('', ProductsListView.as_view(), name='products'),
    path('<uuid:pk>', ProductDetail.as_view(), name='product'),
    path('export-csv/', ExportCSVView.as_view(), name='export_to_csv'),
    path('import-csv/', ProductImportCSVView.as_view(), name='import_to_csv'),
]
