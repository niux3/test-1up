import requests
from bs4 import BeautifulSoup
from slugify import slugify
from collections import namedtuple
from app.get_data_from_csv import get_county, get_average_rent


def get_zipcode(url):
    """retourne le code postal"""
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.select('h1 small').pop().string


def get_cities(county_number, rate=1, living_space=0):
    """retourne la liste des villes d'après l'url spécifiée plus bas"""
    try:
        url = f'https://www.bien-dans-ma-ville.fr/departements/{get_county(str(county_number))}.html'
        r = requests.get(url)
        if r.status_code == 200:
            raw = r.text
            soup = BeautifulSoup(raw, 'html.parser')
            header = soup.select('#villesvoisines table th')
            fields = f"code_postal loyer_moyen {' '.join([slugify(cell.string, separator='_') for cell in header])}"
            City = namedtuple('City', fields)
            len_fields = len(header)

            data = soup.select('#villesvoisines table tr td')
            output = []
            for i, cell in enumerate(data):
                if i % len_fields == 0:
                    row = []
                    city = cell.string
                    zipcode = get_zipcode(cell.find('a')['href'])
                    row.append(zipcode)
                    row.append(get_average_rent(city, rate, living_space))
                    row.append(city)
                elif i % len_fields == len_fields - 1:
                    row.append(cell.string)
                    output.append(City(*row))
                else:
                    row.append(cell.string)
            return output
    except:
        return None


if __name__ == '__main__':
    county = get_county('54')
    print(county)
    print(get_cities(county))
