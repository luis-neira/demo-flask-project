"""
RentalService Module

This module defines the `RentalService` class, which provides methods for managing rental listings. 
It interacts with a datastore to perform CRUD operations on rental properties.
"""

from db import store, Rental
from typing import Union
import sqlite3


class RentalService:
    """ A service class for managing rental listings. """

    def __init__(self):
        conn = sqlite3.connect("real-estate.db")
        self.conn = conn
        self.cursor = conn.cursor()

    def buildResponse(self, rows):
        columns = [column[0] for column in self.cursor.description]
        response = []

        for row in rows:
            response.append(dict(zip(columns, row)))

        return response

    def exists(self, id):
        q1 = "SELECT * FROM rentals WHERE id = ?"
        res = self.cursor.execute(q1, (id,)).fetchone()
        return res is not None

    def find(self, key: str, value: Union[int, str]) -> list[Rental]:
        query = f"SELECT * from rentals WHERE {key} == ?"
        rows = self.cursor.execute(query, (value, )).fetchall()
        return self.buildResponse(rows)

    def get_one_by_id(self, id: int) -> Union[Rental, None]:
        q2 = "SELECT * FROM rentals WHERE id = ?"
        rows = self.cursor.execute(q2, (id, )).fetchone()

        if rows is None:
            return None

        res = self.buildResponse([rows])

        if len(res) > 0:
            return res[0]

        return None

    def get_all(self) -> list[Rental]:
        query = "SELECT * FROM rentals"
        rows = self.cursor.execute(query).fetchall()
        return self.buildResponse(rows)

    def add_one(self, payload) -> Rental:
        record_count = self.cursor.execute(
            "SELECT COUNT(*) FROM rentals"
        ).fetchone()[0]

        new_rental = {"id": record_count + 1, **payload}

        columns = ", ".join(new_rental.keys())  # e.g., "name, age, email"
        placeholders = ", ".join(["?"] * len(new_rental))  # e.g., "?, ?, ?"
        values = tuple(new_rental.values())  # Convert dict values to tuple

        q1 = f"INSERT INTO rentals ({columns}) VALUES ({placeholders})"

        self.cursor.execute(q1, values)
        self.conn.commit()

        inserted_id = self.cursor.lastrowid

        q2 = "SELECT * FROM rentals WHERE id = ?"
        rows = self.cursor.execute(q2, (inserted_id, )).fetchone()
        res = self.buildResponse([rows])
        return res[0]

    def delete_one_by_id(self, id: int) -> bool:
        exists = self.exists(id)

        if not exists:
            return False

        query = "DELETE FROM rentals WHERE id = ?"
        self.cursor.execute(query, (id, ))
        self.conn.commit()

        if self.exists(id) is False:
            return True

        return False

    def update_one_by_id(self, id: int, payload) -> Union[Rental, None]:
        foundRental = self.get_one_by_id(id)

        if foundRental is None:
            return None

        updated_rental = {**foundRental, **payload}
        set_clause = ", ".join([f"{key} = ?" for key in updated_rental.keys()])

        query = f"UPDATE rentals SET {set_clause} WHERE id = {id}"
        self.cursor.execute(query, tuple(updated_rental.values()))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            return updated_rental
        else:
            return None
