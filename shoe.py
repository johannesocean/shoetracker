"""
Created on 2021-07-07 17:45
@author: johannes
"""
from datetime import datetime
from kivy.storage.jsonstore import JsonStore
from utils import get_photo_id, get_kilometers, get_miles


class ShoeStore:
    def __init__(self):
        self.store = JsonStore('data/shoes.json', indent=4)

    def _sync_store(self):
        self.store._is_changed = True
        self.store.store_sync()

    def add_shoe(self, name=None):
        if name:
            self.store.put(
                name,
                time_of_creation=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                accumulated_distance_km=0,
                accumulated_distance_miles=0,
                number_of_runs=0,
                photos=[],
            )

    def add_run(self, name=None, distance=None, miles=False, km=False):
        distance = distance or 0
        if distance:
            distance = round(float(distance.replace(',', '.')), 2)
            added_run = 1 if distance > 0 else -1
        if name:
            self.store._data[name]['accumulated_distance_km'] += distance if km else get_kilometers(distance)
            self.store._data[name]['accumulated_distance_miles'] += distance if miles else get_miles(distance)
            self.store._data[name]['number_of_runs'] += added_run
            self._sync_store()

    # def add_photo(self, name=None, path=None):
    #     if name in self.store and path:
    #         _id = get_photo_id(len(self.store[name]['photos']))
    #         self.store._data[name]['photos'].append({
    #             'name': '_'.join((name, _id)),
    #             'time_of_creation': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #             'comment': '',
    #             'path': path
    #         })
    #         self._sync_store()

    def delete_shoe(self, name=None):
        if name:
            self.store.delete(name)

    @staticmethod
    def _get_shoe_status(km, name=None):
        name = name or ""
        if km < 600:
            return "checkbox-marked-circle", [39 / 256, 174 / 256, 96 / 256, 1], name
        elif km < 900:
            return "alert", [255 / 256, 165 / 256, 0, 1], name
        else:
            return "alert-circle", [1, 0, 0, 1], name

    @property
    def shoe_list(self):
        return sorted(self.store.keys(), key=lambda v: v.upper())

    @property
    def table_data(self):
        data = [
            (
                "",
                self._get_shoe_status(self.store[key]['accumulated_distance_km'], name=key),
                str(self.store[key]['number_of_runs']),
                str(round(self.store[key]['accumulated_distance_km'], 1)),
                # str(round(self.store[key]['accumulated_distance_miles'], 1)),
                self.store[key]['time_of_creation'].split()[0],
                # self._get_shoe_status(self.store[key]['accumulated_distance_km'])
             )
            for key in self.shoe_list
        ]
        if len(data) == 1:
            data.append(("", "", "", "", ""))

        return data
