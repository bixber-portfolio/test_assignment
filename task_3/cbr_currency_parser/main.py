from datetime import datetime, timedelta
from statistics import mean
from tqdm import tqdm
from collections import namedtuple

import requests
from requests.exceptions import (
    HTTPError,
    Timeout,
    ConnectionError,
    RequestException,
)
from bs4 import BeautifulSoup

from utils import display_table
from constants import (
    PERIOD_IN_DAYS,
    URL,
    TIMEOUT_IN_SEC,
    WIDTH_PROGRESS_BAR,
    DATE_FORMAT,
)

today = datetime.today().date()
dates = [
    (today - timedelta(days=i)).strftime(DATE_FORMAT)
    for i in range(
        PERIOD_IN_DAYS,
    )
]

# Создание именованного кортежа для удобного обращения к данным
RateRecord = namedtuple('RateRecord', ['currency', 'date', 'rate'])

rates = {}

for date in tqdm(
    iterable=dates,
    desc=f'Сбор данных по курсам валют за последние {PERIOD_IN_DAYS} дней',
    ncols=WIDTH_PROGRESS_BAR,
):
    url = URL.format(date)
    try:
        resp = requests.get(url, timeout=TIMEOUT_IN_SEC)
        resp.raise_for_status()
    except Timeout:
        print(f'Превышен лимит ожидания при обращении к {url}')
        continue
    except ConnectionError:
        print('Ошибка соединения с сервером')
        continue
    except HTTPError as e:
        print(f'Сервер вернул ошибку {e.response.status_code}')
        continue
    except RequestException as e:
        print(f'Непредвиденная ошибка при запросе к {url}: {e}')
        continue

    soup = BeautifulSoup(resp.content, features='xml')
    for v in soup.find_all('Valute'):
        name = v.Name.text
        value = float(v.Value.text.replace(',', '.'))
        nominal = int(v.Nominal.text)
        rate = value / nominal
        rates.setdefault(name, []).append(RateRecord(name, date, rate))

# соберём все записи в один список [(валюта, дата, курс), ...]
all_data = [record for vals in rates.values() for record in vals]

if not all_data:
    print(
        'Нет данных за последние 90 дней '
        '(проверьте подключение к Интернету или API ЦБ РФ).'
    )
else:
    max_rate = max(all_data, key=lambda x: x.rate)
    min_rate = min(all_data, key=lambda x: x.rate)
    avg_rate = mean(r.rate for r in all_data)
    display_table(
        max_rate=max_rate,
        min_rate=min_rate,
        avg_rate=avg_rate,
    )
