import argparse
import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pprint import pprint

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_winery_age():
    """
    функция принимает число и определяет подходящее окончание
    """

    founding_year = 1920
    founding_date = datetime.datetime(year=founding_year, month=1, day=1)
    today = datetime.datetime.now()
    winery_age = int((today - founding_date).days / 365)

    if 21 > winery_age > 4 or 11 <= winery_age % 100 <= 14:
        return f'Уже {winery_age} лет с вами'

    if winery_age % 10 == 1:
        return f'Уже {winery_age} год с вами'

    if 1 < winery_age % 10 < 5:
        return f'Уже {winery_age} года с вами'

    return f'Уже {winery_age} лет с вами'


def categorization_drinks(wines: list):
    """
    функция принмает словарь c винами, разбивает елементы по категориям и возвращает новый словарь с ключами категориями
    и значениями из изначального словаря
    :param wines:
    :return:
    """

    categorization = defaultdict(list)

    for wine in wines:
        categorization[wine['Категория']].append(wine)

    return dict(categorization)


def main():
    """
    запуск программы
    """

    parser = argparse.ArgumentParser(description='Описание программы')
    parser.add_argument('--path_to_data_file', help='Путь к файлу с карточками вин', default='wine3.xlsx')
    args = parser.parse_args()

    wine_df = pd.read_excel(args.path_to_data_file, na_values=['nan'], keep_default_na=False).to_dict(orient='record')

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        winery_age=get_winery_age(),
        wine_df=categorization_drinks(wine_df)
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
