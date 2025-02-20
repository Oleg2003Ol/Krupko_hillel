from datetime import timedelta

import freezegun
import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from currencies.clients.monobank import MonoBank
from currencies.clients.privatbank import PrivatBank
from currencies.models import CurrencyHistory
from currencies.tasks import get_currencies_task


# def test_get_currencies_task_success(currency_history_factory, mocker):
#     privat_client = mocker.patch(
#         'currencies.clients.privatbank.privatbank_client._prepare_data')
#     assert privat_client.call_count == 0
#     privat_client.return_value = [
#         {'code': 'USD', "buy": "40.55000", "sale": "41.55000"},
#         {'code': 'EUR', "buy": "41.00000", "sale": "42.55000"},
#     ]
#     monobank_client = mocker.patch(
#         'currencies.clients.monobank.monobank_client._prepare_data'
#     )
#     assert monobank_client.call_count == 0
#     monobank_client.return_value = [
#         {'code': 'USD', "buy": "40.55000", "sale": "41.55000"},
#         {'code': 'EUR', "buy": "41.00000", "sale": "42.55000"},
#     ]
#     old = timezone.now() - timedelta(minutes=10)
#     with freezegun.freeze_time(old):
#         currency_history_factory()
#     assert CurrencyHistory.objects.filter(created_at__lte=old).exists()
#     get_currencies_task()
#     assert not CurrencyHistory.objects.filter(created_at__lte=old).exists()
#     assert privat_client.call_count == 1 or monobank_client.call_count == 1
#     if privat_client.call_count == 1:
#         for item in privat_client.return_value:
#             assert CurrencyHistory.objects.filter(
#                 code=item['code'],
#                 buy=item['buy'],
#                 sale=item['sale'],
#             ).exists()
#     elif monobank_client.call_count == 1:
#         for item in monobank_client.return_value:
#             assert CurrencyHistory.objects.filter(
#                 code=item['code'],
#                 buy=item['buy'],
#                 sale=item['sale'],
#             ).exists()

