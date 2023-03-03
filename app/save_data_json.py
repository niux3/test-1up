"""
save json file
"""
import json
import os
import csv
from collections import namedtuple
from requests import get
from bs4 import BeautifulSoup
from slugify import slugify


root = os.path.abspath(os.path.dirname(__file__))


def get_rent(city_name):
    """get rent from csv file"""
    path = os.path.join(root, 'data', 'appartements.csv')
    with open(path, encoding="utf-8") as csv_file:
        try:
            filtered_city = [
                row['loypredm2']
                for row in csv.DictReader(csv_file)
                if row['LIBGEO'] == city_name
            ]
            data = int(filtered_city.pop())
            return data
        except Exception:
            return 42


def get_zipcode(url):
    """retourne le code postal"""
    req = get(url)
    if req.status_code == 200:
        soup = BeautifulSoup(req.text, 'html.parser')
        return soup.select('h1 small').pop().string


def get_county_list_from_http():
    """get cities data"""
    data_to_json = []
    req = get('https://www.bien-dans-ma-ville.fr/departements/')
    if req.status_code == 200:
        soup = BeautifulSoup(req.text, 'html.parser')
        tds = soup.select('#liste table td')
        for td in tds:
            if td.find('a') is not None:
                href = td.find('a')['href']
                req = get(href)
                if req.status_code == 200:
                    soup = BeautifulSoup(req.text, 'html.parser')
                    county_name = td.find('a').string
                    county_code = soup.select('h1 small').pop().string
                    header = soup.select('#villesvoisines table th')
                    default_fields = [
                        slugify(cell.string, separator='_')
                        for cell in header
                    ]
                    str_fields = ' '.join(default_fields)
                    fields = f"code_postal loyer {str_fields}"
                    city_tuple = namedtuple('City', fields)
                    len_fields = len(header)
                    data = soup.select('#villesvoisines table tr td')
                    output_cities = []

                    for i, cell in enumerate(data):
                        if i % len_fields == 0:
                            row = []
                            city_name = cell.string
                            zip_code = get_zipcode(cell.find('a')['href'])
                            params_print = [
                                '> ',
                                county_code,
                                ' > ',
                                city_name,
                                ' > ',
                                zip_code
                            ]
                            print(*params_print)
                            row.append(zip_code)
                            row.append(get_rent(city_name))
                            row.append(city_name)
                        elif i % len_fields == len_fields - 1:
                            row.append(cell.string)
                            output_cities.append(city_tuple(*row)._asdict())
                        else:
                            row.append(cell.string)
                data_to_json.append({
                    county_code: {
                        "name": county_name,
                        "cities": output_cities
                    }
                })
        save_data(data_to_json)


def save_data(rows):
    """save data in folder"""
    path = os.path.join(root, 'data', 'data.json')
    with open(path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(rows, indent=4))


if __name__ == '__main__':
    get_county_list_from_http()
