import decimal
from io import StringIO

import csv
from django import forms
from django.core.exceptions import ValidationError

from products.models import Product, Category


class ImportCSVForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        csv_file = self.cleaned_data['file']
        if not csv_file.name.endswith('.csv'):
            raise ValidationError('This is not a CSV file')
        else:
            reader = csv.DictReader(StringIO(csv_file.read().decode('utf-8')))
            product_list = []
            for product in reader:
                try:
                    category = Category.objects.get(name=product['categories'])
                except Category.DoesNotExist:
                    category = Category.objects.create(name=product['categories'])
                try:
                    new_product = Product.objects.create(
                        name=product['name'],
                        description=product['description'],
                        price=decimal.Decimal(product['price']),
                        sku=product['sku'],
                        is_active=product['is_active'],
                    )
                    new_product.categories.add(category)
                    product_list.append(new_product)
                except (KeyError, decimal.InvalidOperation) as errors:
                    raise ValidationError(errors)
        return product_list

    def save(self):
        product_list = self.cleaned_data['file']
        Product.objects.bulk_create(product_list)
