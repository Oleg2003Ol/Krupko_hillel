import re

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from project.api_base_client import APIBaseClient
import logging


logger = logging.getLogger(__name__)


class Compx(APIBaseClient):
    base_url = 'https://compx.ua/ru/videokarty/'

    def _prepare_data(self) -> list:
        self._request(
            'get',
        )
        results = []
        if self.response and self.response.status_code == 200:
            soup = BeautifulSoup(self.response.content, 'html.parser')
            standart_url = 'https://compx.ua/'
            category = soup.find(
                'div',
                class_='catalog__top-col catalog__top-col--left'
            ).text.strip()
            for item in soup.find_all('div', class_='catalogCard-main-b'):
                try:
                    item_url = urljoin(
                        standart_url,
                        item.find('a', class_='catalogCard-image'
                                  ).get('href'))
                    item_response = requests.get(item_url)
                    res_desc = []
                    if item_response.status_code == 200:
                        item_soup = BeautifulSoup(
                            item_response.content, 'html.parser')
                        for desc in item_soup.find_all('tr',
                                                       'product-features__row'
                                                       ):
                            description_name = desc.find(
                                'th',
                                class_='product-features__cell product-features__cell--h' # noqa
                            ).text.strip()
                            description = desc.find(
                                'td',
                                class_='product-features__cell'
                            ).text.strip()
                            if 'самовывоз' in description_name.lower():
                                continue
                            else:
                                res_desc.append(
                                    f"{description_name}: {description}"
                                )
                    results.append({
                        'image': urljoin(standart_url,
                                         item.find('img').get('src')).strip(),
                        'name': item.find('div',
                                          class_='catalogCard-title'
                                          ).text.strip(),
                        'description': '\n'.join(res_desc),
                        'price': re.sub('[^0-9]', '',
                                        item.find('div',
                                                  class_='catalogCard-price'
                                                  ).text.strip()),
                        'sku': item.find('div',
                                         class_='catalogCard-code'
                                         ).text.replace(
                            'Код товара: ', '').strip(),
                        'category': category
                    })
                except Exception as err:
                    logger.error(err)

        return results

    def parse(self):
        return self._prepare_data()

    def get_image(self, url):
        self._request(
            'get',
            url=url
        )
        return self.response


parser_client = Compx()
