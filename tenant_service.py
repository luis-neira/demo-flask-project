from db import store


class TenantService:
    def __init__(self):
        self.tenants = store["tenants"]

    def get_all_tenants(self):
        return self.tenants

    def get_by_rental_id(self, rental_id):
        tenants = [
            t for t in self.tenants if t["rental_id"] == rental_id
        ]
        return tenants
