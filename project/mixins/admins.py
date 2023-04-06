from django.utils.safestring import mark_safe


class Image:
    def get_image(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="64" height="64" /')
        else:
            return mark_safe('<b>NO IMAGE</b>')

    get_image.short_description = "Image"
