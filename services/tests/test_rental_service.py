import pytest

from db import store
from services import RentalService


@pytest.fixture
def rental_service():
    # Reset the datastore before each test
    store["rentals"].clear()
    mock_data = [
        {"id": 1, "property_type": "apartment", "name": "Downtown Loft"},
        {"id": 2, "property_type": "house", "name": "Suburban Home"},
    ]

    for data in mock_data:
        store["rentals"].append(data)

    return RentalService()


def test_get_all(rental_service):
    rentals = rental_service.get_all()
    assert len(rentals) == 2, "should be 2 rentals"


def test_find(rental_service):
    apartments = rental_service.find("property_type", "apartment")
    assert len(apartments) == 1, "should be 1 apartment rental"
    assert apartments[0]["name"] == "Downtown Loft", "the rental's name should be Downtown Loft"


def test_add_one(rental_service):
    new_rental = {"property_type": "condo", "name": "Luxury Condo"}
    added_rental = rental_service.add_one(new_rental)

    assert added_rental["id"] == 3, "the rental's id should be 3"
    assert added_rental["name"] == "Luxury Condo", "the rental's name should be Luxury Condo"
    assert len(rental_service.get_all()) == 3, "there should be 3 rentals"


def test_get_one_by_id(rental_service):
    rental, index = rental_service.get_one_by_id(2)
    assert rental["name"] == "Suburban Home", "the rental's name should be Suburban Home"
    assert index == 1, "the element should be at index 1"


def test_update_one_by_id(rental_service):
    success, updated_rental = rental_service.update_one_by_id(
        1, {"name": "Modern Loft"})

    assert success is True, "should be True"
    assert updated_rental["name"] == "Modern Loft", "rental's name should be Modern Loft"
    assert rental_service.get_all(
    )[0]["name"] == "Modern Loft", "renatal should be updated in store"


def test_delete_one_by_id(rental_service):
    success = rental_service.delete_one_by_id(1)

    assert success is True, "should be successful"
    assert len(rental_service.get_all()) == 1, "should only by one rental"
    assert rental_service.get_one_by_id(1) is None, "rental should not exist"
