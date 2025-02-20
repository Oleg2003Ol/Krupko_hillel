# Generated by Django 4.1.7 on 2023-05-11 15:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=18)),
                ('code', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('discount_type', models.PositiveSmallIntegerField(choices=[(0, 'Value'), (1, 'Percent')], default=0)),
                ('valid_until', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('order_number', models.PositiveIntegerField(default=1)),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.discount')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=18, validators=[django.core.validators.MinValueValidator(0)])),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='products.product')),
            ],
            options={
                'unique_together': {('order', 'product')},
            },
        ),
        migrations.AddConstraint(
            model_name='order',
            constraint=models.UniqueConstraint(condition=models.Q(('is_active', True)), fields=('user',), name='unique_is_active'),
        ),
    ]
