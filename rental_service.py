from pathlib import Path
import json

raw_data = Path("data.json").read_text()
store = json.loads(raw_data)


class RentalService:
    def __init__(self):
        self.rentals = store["rentals"]

    def find_by_property_type(self, type):
        res = [
            r for r in self.rentals if r["property_type"] == type
        ]
        return res

    def find_by_id(self, data, search_id):
        for i, item in enumerate(data):
            if item['id'] == search_id:
                return (item, i)
        return None

    def get_all_rentals(self):
        return self.rentals

    def add_rental(self, payload):
        new_rental = {"id": len(self.rentals) + 1, **payload}
        self.rentals.append(new_rental)
        return self.rentals[-1]

    def delete_rental(self, id):
        for rental in self.rentals:
            if rental["id"] == id:
                store["rentals"] = [
                    r for r in self.rentals if r["id"] != id
                ]
                return True
        return False

    def update_rental(self, id, payload):
        rental, rentalIdx = self.find_by_id(self.rentals, id)

        if rental is None:
            return (False, None)

        updated_rental = {**rental, **payload}

        self.rentals[rentalIdx] = updated_rental

        return (True, updated_rental)
