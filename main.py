"""
Created on 2021-07-07 17:14
@author: johannes
"""

from kivymd.app import MDApp
from kivy.metrics import dp
from settings import *
from windows import *
from widgets import *
from shoe import *
from pprint import pprint


class MainApp(MDApp):
    """
    """
    data_table = None

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        Settings()
        ThemeTranslator()

        self.theme_cls.primary_palette = ThemeTranslator.get('primary_palette')
        self.theme_cls.theme_style = ThemeTranslator.get('theme_style')
        self.theme_text_color = list(ThemeTranslator.get('theme_text_color'))

        self.shoes = ShoeStore()
        self.shoes.load_store()
        if not self.shoes.shoe_list:
            self.change_setting('selected_shoe', "No shoe selected")

    def on_start(self):
        self.setup_data_table()

    def show_add_shoe_dialog(self, *args):
        dialog = MDDialog(
            title="Add shoe:",
            type="custom",
            content_cls=DialogContentAddShoe(),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                ),
                MDFlatButton(
                    text="Add",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: (self.shoes.add_shoe(name=dialog.content_cls.ids.shoe_name.text),
                                          self._change_shoe_button(dialog.content_cls.ids.shoe_name.text),
                                          dialog.dismiss(), self.update_data_table())
                ),
            ],
        )
        dialog.open()
        pprint(self.shoes['store']._data)

    def show_add_distance_dialog(self):
        dialog = None
        if not self.get_setting('selected_shoe') or self.get_setting('selected_shoe') == "No shoe selected":
            dialog = MDDialog(
                text="No shoes, please add one :)",
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="Add shoe",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: (dialog.dismiss(), self.show_add_shoe_dialog())
                    ),
                ],
            )
        else:
            dialog = MDDialog(
                title="Add distance to {}".format(self.get_setting('selected_shoe')),
                type="custom",
                content_cls=DialogContentAddDistance(),
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="Add",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: (self.shoes.add_run(
                            name=self.get_setting('selected_shoe'),
                            distance=dialog.content_cls.ids.distance_text.text,
                            km=True if self.get_setting('selected_length_unit') == "km" else False,
                            miles=True if self.get_setting('selected_length_unit') == "miles" else False,
                        ), dialog.dismiss(), self.update_data_table())
                    ),
                ],
            )
        dialog.open()

    def open_shoe_menu(self):
        menu = None
        menu_list = [{
            "text": "Add new shoe",
            "viewclass": "IconListItem",
            "icon": "plus-circle-outline",
            "on_release": lambda x=True: (self.show_add_shoe_dialog(x), menu.dismiss())}]
        menu_list = menu_list + [{
                "text": shoe_name,
                "viewclass": "IconListItem",
                "icon": "shoe-sneaker",
                "on_release": lambda x=shoe_name: (self._change_shoe_button(x), menu.dismiss()),
            } for shoe_name in self.shoes.shoe_list]
        menu = MDDropdownMenu(
            caller=self.root.ids.screen_manager.mainwin.ids.shoe_drop_item,
            items=menu_list,
            width_mult=4,
        )
        menu.bind()
        menu.open()

    def setup_data_table(self):
        self.data_table = MDDataTable(
            size_hint=(1, .93),
            use_pagination=True,
            check=False,
            column_data=[
                ("Shoe Name", dp(30)),
                ("Runs", dp(10)),
                ("Km", dp(12)),
                ("Miles", dp(12)),
                ("Added", dp(20)),
                ("Status", dp(10))
            ],
            row_data=self.shoes.table_data,
            sorted_on="Shoe Name",
            # sorted_order="ASC",
            elevation=2
        )
        self.data_table.bind(on_row_press=self.on_row_press)
        self.data_table.bind(on_check_press=self.on_check_press)

        self.root.ids.screen_manager.statswin.ids.stats_table.add_widget(self.data_table)

    def update_data_table(self):
        self.data_table.row_data = self.shoes.table_data

    def _change_shoe_button(self, name):
        self.root.ids.screen_manager.mainwin.ids.shoe_drop_item.text = name
        self.change_setting('selected_shoe', name)

    def switch_to_screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name

    def on_row_press(self, instance_table, instance_row):
        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        print(instance_table, current_row)

    @staticmethod
    def get_setting(key):
        return Settings.get_setting(key)

    @staticmethod
    def change_setting(key, value):
        return Settings.save_setting(key, value)

    def _print(self, *args):
        print(args)


MainApp().run()
