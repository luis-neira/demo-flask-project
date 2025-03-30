from flask import Flask, jsonify, request

from rental_service import RentalService
from tenant_service import TenantService

app = Flask(__name__)

app.json.sort_keys = False


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
    tenant_service = TenantService()

    res = tenant_service.get_by_rental_id(rental_id)

    return jsonify(res)


@app.get("/tenants")
def get_tenants():
    tenant_service = TenantService()

    res = tenant_service.get_all_tenants()

    return jsonify(res)
