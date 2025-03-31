"""
RentalService Module

This module defines the `RentalService` class, which provides methods for managing rental listings. 
It interacts with a datastore to perform CRUD operations on rental properties.
"""

from db import store


class RentalService:
    """ A service class for managing rental listings. """

    def __init__(self):
        """ Initializes the RentalService with rental data from the datastore. """

        self.rentals = store["rentals"]

    def find_by_property_type(self, type):
        """ Finds all rentals that match the given property type. """

        return [
            r for r in self.rentals if r["property_type"] == type
        ]

    def find_by_id(self, data, search_id):
        """ Finds a rental by its unique ID within a given dataset. """

        for i, item in enumerate(data):
            if item['id'] == search_id:
                return (item, i)
        return None

    def get_all_rentals(self):
        """ Retrieves all rentals from the datastore. """

        return self.rentals

    def add_rental(self, payload):
        """ Adds a new rental to the datastore. """

        new_rental = {"id": len(self.rentals) + 1, **payload}
        self.rentals.append(new_rental)
        return self.rentals[-1]

    def delete_rental(self, id):
        """ Deletes a rental from the datastore by its ID. """

        for rental in self.rentals:
            if rental["id"] == id:
                store["rentals"] = [
                    r for r in self.rentals if r["id"] != id
                ]
                return True
        return False

    def update_rental(self, id, payload):
        """ Updates the details of an existing rental """
        rental, rentalIdx = self.find_by_id(self.rentals, id)

        if rental is None:
            return (False, None)

        updated_rental = {**rental, **payload}

        self.rentals[rentalIdx] = updated_rental

        return (True, updated_rental)
