"""
Created on 2021-07-08 18:14
@author: johannes
"""
from kivy.storage.jsonstore import JsonStore


class Settings:
    file_name = 'etc/settings.json'

    def __init__(self):
        pass

    @classmethod
    def save_setting(cls, key, value):
        if key:
            store = JsonStore(cls.file_name, indent=4)
            store.put(key, value=value)

    @classmethod
    def get_setting(cls, key):
        store = JsonStore(cls.file_name, indent=4)
        return store[key].get('value')


class ThemeHandler:
    @classmethod
    def set_theme(cls, theme):
        if theme:
            store = JsonStore('etc/theme.json', indent=4)
            store.put('selected', theme=theme)

    @classmethod
    def get_theme(cls):
        store = JsonStore('etc/theme.json', indent=4)
        return store['selected'].get('theme')


class ThemeTranslator:
    settings_dictionary = {}

    def __init__(self):
        self.update_theme_settings()

    @classmethod
    def update_theme_settings(cls, force=False):
        theme = ThemeHandler.get_theme()
        store = JsonStore('etc/theme.json', indent=4)
        if force or not cls.settings_dictionary:
            for key, item in store._data.items():
                cls.settings_dictionary[key] = item.get(theme)

    @classmethod
    def get(cls, key):
        s = cls.settings_dictionary.get(key)
        return s
