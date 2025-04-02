"""
TenantService Module

This module defines the `TenantService` class, which provides methods for managing tenant records. 
It interacts with a datastore to retrieve tenant information.
"""

from database import get_db


class TenantService:
    """ A service class for managing tenant records. """

    def __init__(self, db=None):
        self._db = db or get_db()
        self.conn = self._db.conn
        self.cursor = self._db.cursor

    def get_all(self):
        query = "SELECT * FROM tenants"
        rows = self.cursor.execute(query).fetchall()
        tenants = [dict(row) for row in rows]
        return tenants

    def find(self, key: str, value):
        query = f"SELECT * FROM tenants WHERE {key} = ?"
        rows = self.cursor.execute(query, (value, )).fetchall()
        tenants = [dict(row) for row in rows]
        return tenants
