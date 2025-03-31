"""
TenantService Module

This module defines the `TenantService` class, which provides methods for managing tenant records. 
It interacts with a datastore to retrieve tenant information.
"""

from db import store


class TenantService:
    """
    A service class for managing tenant records.

    This class provides methods to retrieve all tenants and filter them by rental property.
    """

    def __init__(self):
        """Initializes the TenantService with tenant data from the datastore."""

        self.tenants = store["tenants"]

    def get_all_tenants(self):
        """ Retrieves all tenants from the datastore. """

        return self.tenants

    def get_by_rental_id(self, rental_id):
        """ Finds all tenants associated with a specific rental property. """

        tenants = [
            t for t in self.tenants if t["rental_id"] == rental_id
        ]
        return tenants
