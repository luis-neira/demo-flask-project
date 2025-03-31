"""
TenantService Module

This module defines the `TenantService` class, which provides methods for managing tenant records. 
It interacts with a datastore to retrieve tenant information.
"""

from db import store, Tenant
from typing import Union


class TenantService:
    """ A service class for managing tenant records. """

    __tenants: list[Tenant]

    def __init__(self):
        self.__tenants = store["tenants"]

    def get_all(self) -> list[Tenant]:
        return self.__tenants

    def find(self, key: str, value: Union[int, str]) -> list[Tenant]:
        return [
            t for t in self.__tenants if t.get(key) == value
        ]
