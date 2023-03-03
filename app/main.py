from typing import Union
from app.get_cities import get_cities
from fastapi import FastAPI, HTTPException


app = FastAPI()


@app.get("/")
async def read_root(county: str, rate: int, living_space: int):
    cities = get_cities(county, rate, living_space)
    if cities is None:
        raise HTTPException(status_code=500, detail="Items not found")
    output = []
    for city in cities:
        row = {
            'code postale': city.code_postal,
            'ville': city.ville,
            'population': int(city.habitants.replace(' ', '')),
            'note': float(city.note_globale) if city.note_globale != '-' else city.note_globale,
            'loyer moyen': city.loyer_moyen
        }
        output.append(row)
    return output
