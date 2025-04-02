"""
TenantService Module

This module defines the `TenantService` class, which provides methods for managing tenant records. 
It interacts with a datastore to retrieve tenant information.
"""

from db import store


class TenantService:
    """ A service class for managing tenant records. """

    def __init__(self):
        self.__tenants = store["tenants"]

    def get_all(self):
        return self.__tenants

    def find(self, key: str, value):
        # filter tenants by a given key
        return [
            t for t in self.__tenants if t.get(key) == value
        ]
