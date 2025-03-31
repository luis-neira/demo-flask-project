from pathlib import Path
import json
from dataclasses import dataclass


@dataclass
class Rental:
    id: int
    title: str
    location: str
    price: int
    bedrooms: int
    bathrooms: int
    property_type: str
    description: str
    image: str


@dataclass
class Tenant:
    id: int
    firstname: str
    lastname: str
    email: str
    password: str
    age: int
    rental_id: int


@dataclass
class DataStore:
    rentals: list[Rental]
    tenants: list[Tenant]


def init_db() -> DataStore:
    raw_data = Path("data.json").read_text()
    store = json.loads(raw_data)
    return store


store = init_db()
