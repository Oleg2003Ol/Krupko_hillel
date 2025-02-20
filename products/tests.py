import pytest
from django.urls import reverse

from products.models import Product
from project.constants import MAX_DIGITS, DECIMAL_PLACES
import csv
from django.core.files.uploadedfile import SimpleUploadedFile


def test_products_list(client, faker):
    for _ in range(3):
        Product.objects.create(
            name=faker.word(),
            sku=faker.word(),
            price=faker.pydecimal(
                min_value=0,
                left_digits=DECIMAL_PLACES,
                right_digits=MAX_DIGITS - DECIMAL_PLACES,
            )
        )
    url = reverse('products')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['products']) == Product.objects.count()


def test_export_csv(client, product_factory, user_factory, login_client):
    user = user_factory()
    product_factory.create_batch(5)

    client, _ = login_client(user=user)

    url = reverse('export_to_csv')

    response = client.get(url)
    assert response.status_code == 200
    assert response['Content-Type'] == 'text/csv'
    assert response['Content-Disposition'] == 'attachment; filename="products.csv"'

    content = response.content.decode('utf-8')
    reader = csv.DictReader(content.splitlines())

    expected_fields = ['name', 'description', 'sku', 'image', 'price', 'is_active', 'categories']
    assert reader.fieldnames == expected_fields

    expected_rows_count = 5
    rows_count = sum(1 for _ in reader)
    assert rows_count == expected_rows_count
