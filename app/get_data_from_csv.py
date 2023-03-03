from slugify import slugify
import os
import csv


root = os.path.abspath(os.path.dirname(__file__))


def get_average_rent(city_name, rate, living_space):
    """calcule le loyer moyen"""
    with open(os.path.join(root, 'data', 'appartements.csv')) as csv_file:
        data = int([row['loypredm2'] for row in csv.DictReader(csv_file) if row['LIBGEO'] == city_name].pop())
        # calcul bidon en carton
        result = data * (living_space / rate)
        return result


def get_county(number):
    """retourne le nom d'une ville"""
    with open(os.path.join(root, 'data', 'liste-dpt-drom-com-v1.2.csv')) as csv_file:
        rows = csv.DictReader(csv_file)
        for row in rows:
            code = row['code'] if len(row['code']) > 1 else f"0{row['code']}"
            number = str(number) if len(str(number)) > 1 else f"0{str(number)}"
            if code.upper() == number.upper():
                return slugify(row['nom'].lower())
    return None


if __name__ == '__main__':
    # print(get_county(67))
    c = get_average_rent('Nancy', 800, 50)
    print(c)
