import pytest
from flask import Flask

from resources import bp_rentals
from services import RentalService, TenantService
from main import create_app


@pytest.fixture(scope="class")
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    return app


@pytest.fixture(scope="class")
def client(app):
    return app.test_client()


@pytest.mark.usefixtures("client")
class TestRentals:
    def test_get_rentals(self, client, mocker):
        mocker.patch.object(RentalService, "get_all", return_value=[
            {"id": 1, "property_type": "house"},
            {"id": 2, "property_type": "apartment"}
        ])

        response = client.get("/rentals")
        assert response.status_code == 200
        assert response.get_json() == [
            {"id": 1, "property_type": "house"},
            {"id": 2, "property_type": "apartment"}
        ]

    def test_get_rentals_query_by_house(self, client, mocker):
        mocker.patch.object(RentalService, "find", return_value=[
            {"id": 1, "property_type": "house"},
        ])

        response = client.get("/rentals?type=house")
        assert response.status_code == 200
        assert response.get_json() == [
            {"id": 1, "property_type": "house"},
        ]

    def test_get_rentals_query_by_apartment(self, client, mocker):
        mocker.patch.object(RentalService, "find", return_value=[
            {"id": 2, "property_type": "apartment"},
        ])

        response = client.get("/rentals?type=apartment")
        assert response.status_code == 200
        assert response.get_json() == [
            {"id": 2, "property_type": "apartment"},
        ]

    def test_create_rental(self, client, mocker):
        payload = {
            "title": "Student Studio",
            "location": "Paris, FR",
            "price": 900,
            "bedrooms": 1,
            "bathrooms": 1,
            "property_type": "apartment",
            "description": "Small but functional studio, great for students or holidays in France's capital !",
            "image": "https://www.example.com/student-studio.jpg"
        }

        mocker.patch.object(RentalService, "add_one", return_value={
            "id": 3, **payload
        })

        response = client.post("/rentals", json=payload)
        assert response.status_code == 201
        assert response.get_json() == {"id": 3, **payload}

    def test_delete_rental_by_id_success(self, client, mocker):
        mocker.patch.object(
            RentalService, "delete_one_by_id", return_value=True)
        response = client.delete("/rentals/1")
        assert response.status_code == 200
        assert response.data == b""

    def test_delete_rental_by_id_fail(self, client, mocker):
        mocker.patch.object(
            RentalService, "delete_one_by_id", return_value=False)
        response = client.delete("/rentals/3")
        assert response.status_code == 404
        assert response.get_json() == {"error": "Resource not found."}

    def test_update_rental_success(self, client, mocker):
        payload = {
            "description": "Small but VERY VERY functional studio, great for students or holidays in France's capital !"
        }

        mocker.patch.object(RentalService, "update_one_by_id", return_value=(
            {
                "id": 1,
                "title": "Student Studio",
                "location": "Paris, FR",
                "price": 900,
                "bedrooms": 1,
                "bathrooms": 1,
                "property_type": "apartment",
                "description": "Small but VERY VERY functional studio, great for students or holidays in France's capital !",
                "image": "https://www.example.com/student-studio.jpg"
            }
        ))

        response = client.patch("/rentals/1", json=payload)
        assert response.status_code == 200
        assert response.get_json() == {
            "id": 1,
            "title": "Student Studio",
            "location": "Paris, FR",
            "price": 900,
            "bedrooms": 1,
            "bathrooms": 1,
            "property_type": "apartment",
            "description": "Small but VERY VERY functional studio, great for students or holidays in France's capital !",
            "image": "https://www.example.com/student-studio.jpg"
        }

    def test_update_rental_fail(self, client, mocker):
        mocker.patch.object(
            RentalService,
            "update_one_by_id",
            return_value=None
        )
        response = client.patch(
            "/rentals/3",
            json={
                "description": "Small but VERY VERY functional studio, great for students or holidays in France's capital !"
            }
        )
        assert response.status_code == 500
        assert response.get_json() == {"error": "Something went wrong."}

    def test_get_tenants_by_rental_id(self, client, mocker):
        mocker.patch.object(TenantService, "find", return_value=[
            {"id": 1, "rental_id": 1, "name": "John Doe"}
        ])
        response = client.get("/rentals/1/tenants")
        assert response.status_code == 200
        assert response.get_json() == [
            {"id": 1, "rental_id": 1, "name": "John Doe"}]
