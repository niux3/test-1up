from typing import Union
# from app.get_cities import get_cities
from app.get_data_from_csv import root
from fastapi import FastAPI, HTTPException
import json
import os


app = FastAPI()


@app.get("/")
async def read_root(county_code: str, rate: int, living_space: int):
    output = []
    with open(os.path.join(root, 'data', 'data.json')) as f:
        data_json = json.loads(f.read())
    for i, row in enumerate(data_json):
        if list(row.keys()).pop() == county_code:
            for city in list(row.values()).pop()['cities']:
                output.append({
                    'code postale': city['code_postal'],
                    'ville': city['ville'],
                    'population': int(city['habitants'].replace(' ', '')),
                    'note': float(city['note_globale']) if city['note_globale'] != '-' else city['note_globale'],
                    'loyer moyen': int(city['loyer']) * (living_space / rate)
                })
            return output
        if i == len(data_json) - 1:
            return HTTPException(status_code=404, detail="Item not found")
