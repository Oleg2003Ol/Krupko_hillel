from django.urls import path

from .views import ProductsListView, ExportCSVView, ProductImportCSVView

urlpatterns = [
    path('', ProductsListView.as_view(), name='products'),
    path('export-csv/', ExportCSVView.as_view(), name='export_to_csv'),
    path('import-csv/', ProductImportCSVView.as_view(), name='import_to_csv')
]
