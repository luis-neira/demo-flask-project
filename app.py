from flask import Flask, jsonify, request, abort
from pathlib import Path
import json

app = Flask(__name__)

app.json.sort_keys = False

raw_data = Path("data.json").read_text()
data = json.loads(raw_data)


def find_property_type(type):
    res = [
        r for r in data["rentals"] if r["property_type"] == type
    ]
    return res


def find_by_id(data, search_id):
    for i, item in enumerate(data):
        if item['id'] == search_id:
            return (item, i)
    return None


@app.get("/rentals")
def get_rentals():
    search_word = request.args.get("type")

    if search_word == "house":
        houses = find_property_type("house")
        return jsonify(houses)

    if search_word == "apartment":
        apartments = find_property_type("apartment")
        return jsonify(apartments)

    return jsonify(data["rentals"])


@app.post("/rentals")
def create_rental():
    d = request.get_json()

    data["rentals"].append({"id": len(data["rentals"]) + 1, **d})

    return jsonify(data["rentals"][-1]), 201


@app.delete("/rentals/<int:rental_id>")
def delete_rental(rental_id):
    for rental in data["rentals"]:
        if rental["id"] == rental_id:
            data["rentals"] = [
                r for r in data["rentals"] if r["id"] != rental_id
            ]

            return "", 200

    return jsonify({"error": "Resource not found."}), 404


@app.patch("/rentals/<int:rental_id>")
def update_rental(rental_id):
    new_data = request.get_json()

    rental, rentalIdx = find_by_id(data["rentals"], rental_id)

    if rental is None:
        return jsonify({"error": "Resource not found."}), 404

    updated_rental = {**rental, **new_data}

    data["rentals"][rentalIdx] = updated_rental

    return jsonify(updated_rental), 200


@app.get("/rentals/<int:rental_id>/tenants")
def get_tenants_by_rental_id(rental_id):
    tenants = [
        t for t in data["tenants"] if t["rental_id"] == rental_id
    ]

    return jsonify(tenants)


@app.get("/tenants")
def get_tenants():
    return jsonify(data["tenants"])
