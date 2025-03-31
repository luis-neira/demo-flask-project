"""
TenantService Module

This module defines the `TenantService` class, which provides methods for managing tenant records. 
It interacts with a datastore to retrieve tenant information.
"""

from db import store


class TenantService:
    """ A service class for managing tenant records. """

    def __init__(self):
        """Initializes the TenantService with tenant data from the datastore."""

        self.__tenants = store["tenants"]

    def get_all(self):
        """ Retrieves all tenants from the datastore. """

        return self.__tenants

    def find(self, key, value):
        """ Finds all tenants associated with a specific rental property. """

        return [
            t for t in self.__tenants if t.get(key) == value
        ]
