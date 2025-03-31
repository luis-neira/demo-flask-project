import pytest

from db import store
from services import RentalService


class TestRentalService:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Reset the datastore before each test
        store["rentals"].clear()
        self.mock_data = [
            {"id": 1, "property_type": "apartment", "name": "Downtown Loft"},
            {"id": 2, "property_type": "house", "name": "Suburban Home"},
        ]

        for data in self.mock_data:
            store["rentals"].append(data)

        self.rental_service = RentalService()

    def test_get_all(self):
        rentals = self.rental_service.get_all()
        assert len(rentals) == 2, "should be 2 rentals"

    def test_find(self):
        apartments = self.rental_service.find("property_type", "apartment")
        assert len(apartments) == 1, "should be 1 apartment rental"
        assert apartments[0]["name"] == "Downtown Loft", "the rental's name should be Downtown Loft"

    def test_add_one(self):
        new_rental = {"property_type": "condo", "name": "Luxury Condo"}
        added_rental = self.rental_service.add_one(new_rental)

        assert added_rental["id"] == 3, "the rental's id should be 3"
        assert added_rental["name"] == "Luxury Condo", "the rental's name should be Luxury Condo"

        rental_quantity = len(self.rental_service.get_all())
        assert rental_quantity == 3, "there should be 3 rentals"

    def test_get_one_by_id(self):
        rental, index = self.rental_service.get_one_by_id(2)
        assert rental["name"] == "Suburban Home", "the rental's name should be Suburban Home"
        assert index == 1, "the element should be at index 1"

    def test_update_one_by_id(self):
        success, updated_rental = self.rental_service.update_one_by_id(
            1,
            {"name": "Modern Loft"}
        )

        assert success is True, "should be True"
        assert updated_rental["name"] == "Modern Loft", "rental's name should be Modern Loft"

        rental_name = self.rental_service.get_all()[0]["name"]
        assert rental_name == "Modern Loft", "rental should be updated in store"

    def test_delete_one_by_id(self):
        success = self.rental_service.delete_one_by_id(1)

        assert success is True, "should be successful"

        rental_quantity = len(self.rental_service.get_all())
        assert rental_quantity == 1, "should only be one rental"

        rental = self.rental_service.get_one_by_id(1)
        assert rental is None, "rental should not exist"
