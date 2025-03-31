from flask import Flask, jsonify, request

from services import TenantService, RentalService

app = Flask(__name__)

app.json.sort_keys = False


@app.get("/rentals")
def get_rentals():
    query_by = request.args.get("type")

    rental_service = RentalService()

    HOUSE, APARTMENT = "house", "apartment"

    if query_by == HOUSE:
        houses = rental_service.find("property_type", HOUSE)
        return jsonify(houses)

    if query_by == APARTMENT:
        apartments = rental_service.find("property_type", APARTMENT)
        return jsonify(apartments)

    res = rental_service.get_all()

    return jsonify(res)


@app.post("/rentals")
def create_rental():
    body = request.get_json()

    rental_service = RentalService()

    res = rental_service.add_one(body)

    return jsonify(res), 201


@app.delete("/rentals/<int:rental_id>")
def delete_one_by_id(rental_id):
    rental_service = RentalService()

    success = rental_service.delete_one_by_id(rental_id)

    if success == False:
        return jsonify({"error": "Resource not found."}), 404

    return "", 200


@app.patch("/rentals/<int:rental_id>")
def update_rental(rental_id):
    body = request.get_json()

    rental_service = RentalService()

    success, updated_data = rental_service.update_one_by_id(
        rental_id,
        body
    )

    if success == False:
        return jsonify({"error": "Something wnet wrong."}), 400

    return jsonify(updated_data), 200


@app.get("/rentals/<int:rental_id>/tenants")
def get_tenants_by_rental_id(rental_id):
    tenant_service = TenantService()

    res = tenant_service.find("rental_id", rental_id)

    return jsonify(res)


@app.get("/tenants")
def get_tenants():
    tenant_service = TenantService()

    res = tenant_service.get_all()

    return jsonify(res)
