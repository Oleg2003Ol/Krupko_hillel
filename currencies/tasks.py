from datetime import timedelta

from celery import shared_task
from django.core.exceptions import ValidationError
from django.utils import timezone

from currencies.clients.monobank import monobank_client
from currencies.clients.privatbank import privatbank_client
from currencies.models import CurrencyHistory
from project.celery import app


@app.task
def delete_old_currencies():
    CurrencyHistory.objects.filter(
        created_at__lt=timezone.now() - timedelta(days=3)
    ).delete()


@shared_task
def get_currencies_task():
    clients = [privatbank_client, monobank_client]

    for client in clients:
        client_data = client.save()
        if client_data:
            results = []
            for i in client_data:
                results.append(
                    CurrencyHistory(
                        **i
                    )
                )
            if results:
                CurrencyHistory.objects.bulk_create(results)
            break
    else:
        raise ValidationError('No bank client.')
