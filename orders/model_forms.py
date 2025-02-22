from django import forms
from django.core.exceptions import ValidationError

from orders.models import OrderItem, Discount
from products.models import Product


class CartForm(forms.Form):
    discount = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)
        self.fields.update({k: forms.IntegerField() if k.startswith(
            'quantity') else forms.UUIDField() for k in self.data.keys() if
                            k.startswith(('quantity', 'item'))})

    def clean_discount(self):
        if self.cleaned_data['discount']:
            try:
                discount = Discount.objects.get(
                    code=self.cleaned_data['discount']
                )
                if not discount.is_valid:
                    raise ValidationError
            except (Discount.DoesNotExist, ValidationError):
                raise ValidationError('Invalid discount code.')
            return discount

    def save(self):
        for k in self.cleaned_data.keys():
            if k.startswith('item_'):
                index = k.split('_')[-1]
                try:
                    item = OrderItem.objects.select_for_update().get(
                        id=self.cleaned_data[f'item_{index}']
                    )
                except OrderItem.DoesNotExist:
                    raise ValidationError('Something wrong!')
                item.quantity = self.cleaned_data[f'quantity_{index}']
                item.save(update_fields=('quantity',))
        discount = self.cleaned_data.get('discount')
        if discount:
            self.instance.discount = discount
            self.instance.save(update_fields=('discount',))
        return self.instance


class CartActionForm(forms.Form):
    product_id = forms.UUIDField(required=False)
    order_item_id = forms.UUIDField(required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)

    def clean_product_id(self):
        if self.cleaned_data['product_id']:
            try:
                return Product.objects.get(id=self.cleaned_data['product_id'])
            except Product.DoesNotExist:
                raise ValidationError('Wrong product id.')

    def clean_order_item_id(self):
        if self.cleaned_data.get('order_item_id') and \
                not self.instance.order_items.filter(
                    id=self.cleaned_data['order_item_id']
                ).exists():
            raise ValidationError('Wrong item id.')
        return self.cleaned_data['order_item_id']

    def action(self, action):
        if action == 'add':
            product = self.cleaned_data['product_id']
            try:
                order_item = OrderItem.objects.get(order=self.instance,
                                                   product=product)
                order_item.price = product.price
                order_item.save()
            except OrderItem.DoesNotExist:
                order_item = OrderItem.objects.create(order=self.instance,
                                                      product=product,
                                                      price=product.price)

            if not OrderItem.DoesNotExist:
                order_item.quantity += 1
                order_item.save()
            # messages.success(request, 'Product added to cart!')

        if action == 'pay':
            self.instance.is_active = False
            self.instance.is_paid = True
            self.instance.save(update_fields=('is_active', 'is_paid'))
            # messages.success(request, 'Order successfully paid!')

        if action == 'remove':
            OrderItem.objects.filter(
                id=self.cleaned_data['order_item_id']
            ).delete()
            # messages.success(request, 'Item successfully removed from cart!')
        if action == 'clear':
            self.instance.order_items.all().delete()
            # messages.success(request,
            # 'All items have been removed from the cart!')
