import pytest
from flask import Flask

from resources import bp_rentals
from services import RentalService, TenantService


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(bp_rentals, url_prefix="/rentals")
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_rentals(client, mocker):
    mocker.patch.object(RentalService, "get_all", return_value=[
        {"id": 1, "property_type": "house"},
        {"id": 2, "property_type": "apartment"}
    ])

    response = client.get("/rentals")

    assert response.status_code == 200, "status code should be 200"
    assert response.get_json() == [
        {"id": 1, "property_type": "house"},
        {"id": 2, "property_type": "apartment"}
    ], "should respond with correct payload"


def test_create_rental(client, mocker):
    mocker.patch.object(RentalService, "add_one", return_value={
        "id": 3, "property_type": "house"
    })

    response = client.post("/rentals", json={"property_type": "house"})

    assert response.status_code == 201, "status code should be 201"
    assert response.get_json() == {
        "id": 3, "property_type": "house"
    }, "should respond with correct payload"


def test_delete_rental_by_id(client, mocker):
    mocker.patch.object(RentalService, "delete_one_by_id", return_value=True)

    response = client.delete("/rentals/1")

    assert response.status_code == 200, "status code should be 200"
    assert response.data == b"", "payload should be an empty string"


def test_update_rental(client, mocker):
    mocker.patch.object(RentalService, "update_one_by_id", return_value=(
        True, {"id": 1, "property_type": "apartment"}))

    response = client.patch("/rentals/1", json={"property_type": "apartment"})

    assert response.status_code == 200, "status code should be 200"
    assert response.get_json() == {
        "id": 1, "property_type": "apartment"
    }, "should respond with correct payload"


def test_get_tenants_by_rental_id(client, mocker):
    mocker.patch.object(TenantService, "find", return_value=[
        {"id": 1, "rental_id": 1, "name": "John Doe"}
    ])

    response = client.get("/rentals/1/tenants")

    assert response.status_code == 200, "status code should be 200"
    assert response.get_json() == [
        {"id": 1, "rental_id": 1, "name": "John Doe"}
    ], "should respond with correct payload"
