from django.contrib import admin

from products.models import Product, Category
from project.mixins.admins import ImageAdminMixin


@admin.register(Product)
class ProductAdmin(ImageAdminMixin, admin.ModelAdmin):
    list_display = ("name", "is_active")
    filter_horizontal = ("categories", "products")


@admin.register(Category)
class CategoryAdmin(ImageAdminMixin, admin.ModelAdmin):
    ...
