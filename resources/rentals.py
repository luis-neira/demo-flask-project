from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError

from services import RentalService, TenantService


class RentalCreationSchema(Schema):
    title = fields.Str(required=True)
    location = fields.Str(required=True)
    price = fields.Int(required=True)
    bedrooms = fields.Int(required=True)
    bathrooms = fields.Int(required=True)
    property_type = fields.Str(required=True)
    description = fields.Str(required=True)
    image = fields.Str(required=True)


class RentalUpdateSchema(Schema):
    title = fields.Str()
    location = fields.Str()
    price = fields.Int()
    bedrooms = fields.Int()
    bathrooms = fields.Int()
    property_type = fields.Str()
    description = fields.Str(required=True)
    image = fields.Str()


bp = Blueprint('rentals', __name__)


@bp.get("")
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


@bp.post("")
def create_rental():
    try:
        schema = RentalCreationSchema()

        body = schema.load(request.get_json())

        rental_service = RentalService()

        res = rental_service.add_one(body)

        return jsonify(res), 201
    except ValidationError as err:
        return jsonify({"error": "Invalid data", "fields": err.messages}), 400


@bp.delete("/<int:id>")
def delete_rental_by_id(id):
    rental_service = RentalService()

    success = rental_service.delete_one_by_id(id)

    if success == False:
        return jsonify({"error": "Resource not found."}), 404

    return "", 200


@bp.patch("/<int:id>")
def update_rental(id):
    try:
        schema = RentalUpdateSchema()

        body = schema.load(request.get_json())

        rental_service = RentalService()

        updated_data = rental_service.update_one_by_id(
            id,
            body
        )

        if updated_data is None:
            return jsonify({"error": "Something went wrong."}), 500

        return jsonify(updated_data), 200
    except ValidationError as err:
        return jsonify({"error": "Invalid data", "fields": err.messages}), 400


@bp.get("/<int:rental_id>/tenants")
def get_tenants_by_rental_id(rental_id):
    tenant_service = TenantService()

    res = tenant_service.find("rental_id", rental_id)

    return jsonify(res)
