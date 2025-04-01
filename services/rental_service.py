"""
RentalService Module

This module defines the `RentalService` class, which provides methods for managing rental listings. 
It interacts with a datastore to perform CRUD operations on rental properties.
"""

from db import store, Rental
from typing import Union, Any, cast


class RentalService:
    """ A service class for managing rental listings. """

    __rentals: list[Rental]

    def __init__(self):
        self.__rentals = store["rentals"]

    def find(self, key: str, value: Union[int, str]) -> list[Rental]:
        # filter rentals by a given key
        return [
            r for r in self.__rentals if r.get(key) == value
        ]

    def get_one_by_id(self, id: int) -> Union[tuple[Rental, int], None]:
        for i, item in enumerate(self.__rentals):
            if item['id'] == id:
                return (item, i)

        return None

    def get_all(self) -> list[Rental]:
        return self.__rentals

    def add_one(self, payload: Any) -> Rental:
        new_rental = cast(Rental, {"id": len(self.__rentals) + 1, **payload})
        self.__rentals.append(new_rental)

        return self.__rentals[-1]

    def delete_one_by_id(self, id: int) -> bool:
        for i, rental in enumerate(self.__rentals):
            if rental["id"] == id:
                del self.__rentals[i]
                return True

        return False

    def update_one_by_id(self, id: int, payload: Any) -> tuple[bool, Union[None, Rental]]:
        # rental, rentalIdx = self.get_one_by_id(id)
        foundRental = self.get_one_by_id(id)

        if foundRental is None:
            return (False, None)

        rental, rentalIdx = foundRental

        updated_rental = cast(Rental, {**rental, **payload})
        self.__rentals[rentalIdx] = updated_rental

        return (True, updated_rental)
