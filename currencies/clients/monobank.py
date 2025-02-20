from currencies.models import CurrencyHistory
from project.api_base_client import APIBaseClient


class MonoBank(APIBaseClient):
    base_url = 'https://api.monobank.ua/bank/currency'

    def _prepare_data(self) -> list:
        self._request(
            'get',
        )
        results = []
        if self.response:
            for i in self.response.json():
                if i['currencyCodeA'] == 840 and i['currencyCodeB'] == 980:
                    results.append({
                        'code': 'USD',
                        'buy': i['rateBuy'],
                        'sale': i['rateSell'],
                    })
                elif i['currencyCodeA'] == 978 and i['currencyCodeB'] == 980:
                    results.append({
                        'code': 'EUR',
                        'buy': i['rateBuy'],
                        'sale': i['rateSell'],
                    })
        return results

    def save(self):
        results = []
        for i in self._prepare_data():
            results.append(
                CurrencyHistory(
                    **i
                )
            )
        if results:
            CurrencyHistory.objects.bulk_create(results)


monobank_client = MonoBank()
