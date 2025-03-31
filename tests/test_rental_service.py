import pytest

from db import store  # Import the store to manipulate test data
from services import RentalService


@pytest.fixture
def rental_service():
    """Fixture to create a fresh RentalService instance before each test."""
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
    """Test retrieving all rentals."""

    rentals = rental_service.get_all()
    assert len(rentals) == 2


def test_find(rental_service):
    """Test filtering rentals by property type."""

    apartments = rental_service.find("property_type", "apartment")
    assert len(apartments) == 1
    assert apartments[0]["name"] == "Downtown Loft"


def test_add_one(rental_service):
    """Test adding a new rental."""

    new_rental = {"property_type": "condo", "name": "Luxury Condo"}
    added_rental = rental_service.add_one(new_rental)

    assert added_rental["id"] == 3  # IDs should increment
    assert added_rental["name"] == "Luxury Condo"
    assert len(rental_service.get_all()) == 3


def test_get_one_by_id(rental_service):
    """Test finding a rental by ID."""

    rental, index = rental_service.get_one_by_id(2)
    assert rental["name"] == "Suburban Home"
    assert index == 1


def test_update_one_by_id(rental_service):
    """Test updating a rental."""

    success, updated_rental = rental_service.update_one_by_id(
        1, {"name": "Modern Loft"})

    assert success is True
    assert updated_rental["name"] == "Modern Loft"
    assert rental_service.get_all()[0]["name"] == "Modern Loft"


def test_delete_one_by_id(rental_service):
    """Test deleting a rental."""

    success = rental_service.delete_one_by_id(1)

    assert success is True
    assert len(rental_service.get_all()) == 1
    assert rental_service.get_one_by_id(1) is None
