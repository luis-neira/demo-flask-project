from flask import Blueprint, jsonify

bp = Blueprint('root', __name__)


@bp.get("/")
def health_check():
    return jsonify({
        "status": "API is running",
        "available_endpoints": ["/rentals", "/tenants"]
    })
