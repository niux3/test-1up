from get_cities import get_zipcode
from get_data_from_csv import root, get_rent
from requests import get
from bs4 import BeautifulSoup
from slugify import slugify
from collections import namedtuple
import json
import os


def get_county_list_from_http():
    data_to_json = []
    r = get('https://www.bien-dans-ma-ville.fr/departements/')
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        tds = soup.select('#liste table td')
        for td in tds:
            if td.find('a') is not None:
                href = td.find('a')['href']
                r = get(href)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    county_name = td.find('a').string
                    county_code = soup.select('h1 small').pop().string
                    header = soup.select('#villesvoisines table th')
                    fields = f"code_postal loyer {' '.join([slugify(cell.string, separator='_') for cell in header])}"
                    City = namedtuple('City', fields)
                    len_fields = len(header)
                    data = soup.select('#villesvoisines table tr td')
                    output_cities = []

                    for i, cell in enumerate(data):
                        if i % len_fields == 0:
                            row = []
                            city = cell.string
                            zip_code = get_zipcode(cell.find('a')['href'])
                            print('>>> ', county_code, ' >> ', city, ' >> ', zip_code)
                            row.append(zip_code)
                            row.append(get_rent(city))
                            row.append(city)
                        elif i % len_fields == len_fields - 1:
                            row.append(cell.string)
                            output_cities.append(City(*row)._asdict())
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
    print(root)
    with open(os.path.join(root, 'data', 'data.json'), 'w') as f:
        f.write(json.dumps(rows, indent=4))


if __name__ == '__main__':
    get_county_list_from_http()
