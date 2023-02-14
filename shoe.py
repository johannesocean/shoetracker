"""
Created on 2021-07-07 17:45
@author: johannes
"""
from db import get_db, write_to_db
from utils import get_time_now, thread_process


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
        client_shoes = self.page.client_storage.get('shoes')
        db = get_db()
        if db:
            # FIXME add user
            db_shoes = db.get('shoes')
            if client_shoes != db_shoes:
                self.page.client_storage.set('shoes', db_shoes or {})

    def add_shoe(self, name: str):
        if not name:
            return
        shoes = self.page.client_storage.get('shoes') or {}
        shoes.setdefault(name, get_new_shoe_data(name))
        self.page.client_storage.set('shoes', shoes)
        self.set_selected_shoe(name)
        thread_process(write_to_db, shoes=shoes)

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
        thread_process(write_to_db, shoes=shoes)

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
        name = name or ""
        self.page.client_storage.set('selected', name)
        thread_process(write_to_db, selected=name)

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
