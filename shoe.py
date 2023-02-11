"""
Created on 2021-07-07 17:45
@author: johannes
"""
from utils import get_time_now


def get_new_shoe_data(name):
    return {
        "name": name,
        "time_of_creation": get_time_now(),
        "accumulated_distance_km": 0,
        "number_of_runs": 0
    }


class DataHandler:
    def __init__(self, page):
        self.page = page

    def add_shoe(self, name: str):
        if not name:
            return
        shoes = self.page.client_storage.get('shoes') or {}
        shoes.setdefault(name, get_new_shoe_data(name))
        self.page.client_storage.set('shoes', shoes)
        self.set_selected_shoe(name)

    def add_distance_to_shoe(self, name: str, distance=None):
        if not name:
            return
        try:
            distance = float(distance.replace(',', '.'))
        except ValueError:
            return
        shoes = self.page.client_storage.get('shoes')
        shoes[name]["accumulated_distance_km"] += distance
        shoes[name]["number_of_runs"] += 1
        self.page.client_storage.set('shoes', shoes)

    def get_shoe(self, name: str):
        shoes = self.page.client_storage.get('shoes') or {}
        return shoes.get(name) or {}

    def get_all_shoes(self):
        return self.page.client_storage.get('shoes') or {}

    def get_shoe_list(self):
        shoes = self.page.client_storage.get('shoes')
        return list(shoes if shoes else [])

    def get_selected_shoe(self):
        return self.page.client_storage.get('selected') or ""

    def set_selected_shoe(self, name):
        self.page.client_storage.set('selected', name or "")

    # def delete_shoe(self, name=None):
    #     if name:
    #         self.store.delete(name)
    #
    # @staticmethod
    # def _get_shoe_status(km, name=None):
    #     name = name or ""
    #     if km < 600:
    #         return "checkbox-marked-circle", [39 / 256, 174 / 256, 96 / 256, 1], name
    #     elif km < 900:
    #         return "alert", [255 / 256, 165 / 256, 0, 1], name
    #     else:
    #         return "alert-circle", [1, 0, 0, 1], name
