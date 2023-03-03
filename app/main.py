"""
fichier d'execution fastapi
"""
import json
import os
from fastapi import FastAPI, HTTPException
from app.save_data_json import root


app = FastAPI()


@app.get("/")
async def read_root(county_code: str, rate: int, living_space: int):
    """index project"""
    output = []
    path = os.path.join(root, 'data', 'data.json')
    with open(path, encoding="utf-8") as file:
        data_json = json.loads(file.read())
    for i, row in enumerate(data_json):
        if list(row.keys()).pop() == county_code:
            for city in list(row.values()).pop()['cities']:
                note = city['note_globale']
                output.append({
                    'code postale': city['code_postal'],
                    'ville': city['ville'],
                    'population': int(city['habitants'].replace(' ', '')),
                    'note': float(note) if note != '-' else note,
                    'loyer moyen': int(city['loyer']) * (living_space / rate)
                })
            return output
        if i == len(data_json) - 1:
            raise HTTPException(status_code=404, detail="Item not found")
