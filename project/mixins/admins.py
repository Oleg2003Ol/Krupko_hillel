from django.utils.safestring import mark_safe


class ImageAdminMixin:
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return readonly_fields + ['image_field']

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return ('image_field',) + list_display

    @mark_safe
    def image_field(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}'
                             f'"width="64" height="64"')
        else:
            return mark_safe('<b>NO IMAGE</b>')
