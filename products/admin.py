from django.contrib import admin
from django.utils.safestring import mark_safe

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("get_image", "name", "is_active")
    readonly_fields = ("get_image",)

    @admin.display(description='Image')
    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="64" height="64"')

