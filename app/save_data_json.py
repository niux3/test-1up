"""
save json file
"""
import json
import os
from collections import namedtuple
from get_cities import get_zipcode
from get_data_from_csv import root, get_rent
from requests import get
from bs4 import BeautifulSoup
from slugify import slugify


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
                            city = cell.string
                            zip_code = get_zipcode(cell.find('a')['href'])
                            params_print = [
                                '> ',
                                county_code,
                                ' > ',
                                city,
                                ' > ',
                                zip_code
                            ]
                            print(*params_print)
                            row.append(zip_code)
                            row.append(get_rent(city))
                            row.append(city)
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
                # if county_code == '01':
                #     pprint(data_to_json, indent=2)
                #     break
        save_data(data_to_json)


def save_data(rows):
    """save data in folder"""
    path = os.path.join(root, 'data', 'data.json')
    with open(path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(rows, indent=4))


if __name__ == '__main__':
    get_county_list_from_http()
