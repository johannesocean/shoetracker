from db import read_from_db, write_to_db
from utils import get_time_now, thread_process


def get_new_shoe_data(name):
    return {
        "name": name,
        "time_of_creation": get_time_now(),
        "accumulated_distance_km": 0,
        "number_of_runs": 0
    }


# TODO remove hardcoded colors --> to theme config file.


class DataHandler:
    def __init__(self, page):
        self.page = page
        db_shoes = read_from_db('shoes')
        # FIXME add user
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
