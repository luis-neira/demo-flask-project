from flask import Blueprint, jsonify, g

from services import TenantService

bp = Blueprint('tenants', __name__)


@bp.get("")
def get_tenants():
    tenant_service = TenantService()

    res = tenant_service.get_all()

    return jsonify(res)
