"""
RentalService Module

This module defines the `RentalService` class, which provides methods for managing rental listings. 
It interacts with a datastore to perform CRUD operations on rental properties.
"""

from database import get_db


class RentalService:
    """ A service class for managing rental listings. """

    def __init__(self):
        self.conn = get_db().conn
        self.cursor = get_db().cursor

    def exists(self, id):
        q1 = "SELECT * FROM rentals WHERE id = ?"
        res = self.cursor.execute(q1, (id,)).fetchone()
        return res is not None

    def find(self, key, value):
        query = f"SELECT * from rentals WHERE {key} == ?"
        rows = self.cursor.execute(query, (value, )).fetchall()
        rentals = [dict(row) for row in rows]
        return rentals

    def get_one_by_id(self, id):
        q2 = "SELECT * FROM rentals WHERE id = ?"
        row = self.cursor.execute(q2, (id, )).fetchone()

        if row is None:
            return None

        return dict(row)

    def get_all(self):
        query = "SELECT * FROM rentals"
        rows = self.cursor.execute(query).fetchall()
        rentals = [dict(row) for row in rows]
        return rentals

    def add_one(self, payload):
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
        row = self.cursor.execute(q2, (inserted_id, )).fetchone()
        return dict(row)

    def delete_one_by_id(self, id):
        exists = self.exists(id)

        if not exists:
            return False

        query = "DELETE FROM rentals WHERE id = ?"
        self.cursor.execute(query, (id, ))
        self.conn.commit()

        if self.exists(id) is False:
            return True

        return False

    def update_one_by_id(self, id, payload):
        foundRental = self.get_one_by_id(id)

        if foundRental is None:
            return None

        updated_rental = {**foundRental, **payload}
        set_clause = ", ".join([f"{key} = ?" for key in updated_rental.keys()])

        query = f"UPDATE rentals SET {set_clause} WHERE id = ?"
        self.cursor.execute(query, tuple(updated_rental.values()) + (id,))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            return updated_rental
        else:
            return None
