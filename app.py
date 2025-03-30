from flask import Flask, jsonify, request, abort
from pathlib import Path
import json

from rental_service import RentalService

app = Flask(__name__)

app.json.sort_keys = False

raw_data = Path("data.json").read_text()
data = json.loads(raw_data)


# def find_property_type(type):
#     res = [
#         r for r in data["rentals"] if r["property_type"] == type
#     ]
#     return res


# def find_by_id(data, search_id):
#     for i, item in enumerate(data):
#         if item['id'] == search_id:
#             return (item, i)
#     return None


@app.get("/rentals")
def get_rentals():
    search_word = request.args.get("type")

    rental_service = RentalService()

    if search_word == "house":
        houses = rental_service.find_by_property_type("house")
        return jsonify(houses)

    if search_word == "apartment":
        apartments = rental_service.find_by_property_type("apartment")
        return jsonify(apartments)

    res = rental_service.get_all_rentals()

    return jsonify(res)


@app.post("/rentals")
def create_rental():
    data = request.get_json()

    rental_service = RentalService()

    res = rental_service.add_rental(data)

    return jsonify(res), 201


@app.delete("/rentals/<int:rental_id>")
def delete_rental(rental_id):
    rental_service = RentalService()

    success = rental_service.delete_rental(rental_id)

    if success == False:
        return jsonify({"error": "Resource not found."}), 404

    return "", 200


@app.patch("/rentals/<int:rental_id>")
def update_rental(rental_id):
    new_data = request.get_json()

    rental_service = RentalService()

    res = rental_service.update_rental(rental_id, new_data)

    return jsonify(res), 200


@app.get("/rentals/<int:rental_id>/tenants")
def get_tenants_by_rental_id(rental_id):
    tenants = [
        t for t in data["tenants"] if t["rental_id"] == rental_id
    ]

    return jsonify(tenants)


@app.get("/tenants")
def get_tenants():
    return jsonify(data["tenants"])
