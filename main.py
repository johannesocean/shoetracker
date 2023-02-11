"""
Created on 2021-07-07 17:14
@author: johannes
"""
import flet as ft
# from settings import *
from shoe import *
from utils import *

APPBAR_TITLES = {
    "home": ft.Text(""),
    "statistic": ft.Text("Shoe stats"),
}


def get_new_shoe_data():
    return {
        "time_of_creation": get_time_now(),
        "accumulated_distance_km": 0,
        "number_of_runs": 0
    }


class DataHandler:
    def __init__(self, page: ft.Page):
        self.page = page

    def add_shoe(self, name: str):
        shoes = self.page.client_storage.get('shoes') or {}
        shoes.setdefault(name, get_new_shoe_data())
        self.page.client_storage.set('shoes', shoes)
        self.set_selected_shoe(name)

    def add_distance_to_shoe(self, name, distance=None):
        try:
            distance = float(distance.replace(',', '.'))
        except:
            return
        shoes = self.page.client_storage.get('shoes')
        shoes[name]["accumulated_distance_km"] += distance
        shoes[name]["number_of_runs"] += 1
        self.page.client_storage.set('shoes', shoes)

    def get_shoe(self, name: str):
        shoes = self.page.client_storage.get('shoes') or {}
        return shoes.get(name) or {}

    def get_shoe_list(self):
        shoes = self.page.client_storage.get('shoes')
        return list(shoes if shoes else [])

    def get_selected_shoe(self):
        return self.page.client_storage.get('selected') or ""

    def set_selected_shoe(self, name):
        self.page.client_storage.set('selected', name)


def main(page: ft.Page):
    page.title = "Shoetracker"
    data_handler = DataHandler(page)

    class AppBarSpecified(ft.AppBar):
        def __init__(self, title: str = None):
            super().__init__(
                leading_width=40,
                title=ft.Text(title),
                actions=[
                    ft.IconButton(ft.icons.BAR_CHART_SHARP, on_click=lambda _: layout_change("statistic")),
                    ft.IconButton(ft.icons.HOME_SHARP, on_click=lambda _: layout_change("home"))
                ]
            )

    def layout_change(page_name):
        page.appbar.title = APPBAR_TITLES.get(page_name)
        page.controls = []
        if page_name == "home":
            add_item(home_content)
        elif page_name == "statistic":
            ...
            # add_item(text_field, list_view)

        if page_name != "statistic":
            ...
        page.update()

    def remove_item(*items):
        for item in items:
            if item in page.controls:
                page.controls.remove(item)
        page.update()

    def add_item(*items):
        for item in items:
            if item not in page.controls:
                page.controls.append(item)
        page.update()

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def add_and_close_dlg(e):
        if new_shoe_text.value:
            data_handler.add_shoe(new_shoe_text.value)
            shoes_dropdown.options.append(ft.dropdown.Option(new_shoe_text.value))
            shoes_dropdown.value = new_shoe_text.value
            distance_dlg_modal.title = f"Add distance to {new_shoe_text.value}"
            new_shoe_text.value = ""
        dlg_modal.open = False
        page.update()

    def close_dlg(e):
        dlg_modal.open = False
        distance_dlg_modal.open = False
        page.update()

    def open_distance_dlg_modal(e):
        page.dialog = distance_dlg_modal
        distance_dlg_modal.open = True
        page.update()

    def add_distance_dlg(e):
        if distance_text.value:
            data_handler.add_shoe(new_shoe_text.value)
            distance_text.value = ""
        dlg_modal.open = False
        page.update()

    def on_dropdown_change(e):
        data_handler.set_selected_shoe(shoes_dropdown.value)
        distance_dlg_modal.title = ft.Text(f"Add distance to {shoes_dropdown.value}")

    new_shoe_text = ft.TextField(helper_text="Example: Sense Ride 4")
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Add new shoe"),
        content=new_shoe_text,
        actions=[
            ft.TextButton("Add", on_click=add_and_close_dlg),
            ft.TextButton("Cancel", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    shoes_dropdown = ft.Dropdown(options=[ft.dropdown.Option(_shoe) for _shoe in data_handler.get_shoe_list()],
                                 value=data_handler.get_selected_shoe(),
                                 on_change=on_dropdown_change)
    add_shoe_button = ft.ElevatedButton("Add new shoe", on_click=open_dlg_modal)

    distance_text = ft.TextField(helper_text="Km - Example: 17.3")
    distance_dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text(f"Add distance to {data_handler.get_selected_shoe()}"),
        content=distance_text,
        actions=[
            ft.TextButton("Add", on_click=add_distance_dlg),
            ft.TextButton("Cancel", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    add_distance_button = ft.ElevatedButton(
        "Add distance to shoe!",
        icon=ft.icons.RUN_CIRCLE_ROUNDED,
        icon_color="green400",
        on_click=open_distance_dlg_modal
    )

    home_content = ft.Column(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Row(
                                [shoes_dropdown, add_shoe_button],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=add_distance_button,
                            alignment=ft.alignment.center
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY
                ), height=400
            )
        ]
    )

    page.appbar = AppBarSpecified()
    add_item(home_content)


ft.app(
    port=8080,
    target=main,
    assets_dir="assets",
    view=ft.WEB_BROWSER
)

# class MainApp(MDApp):
#     """
#     """
#     data_table = None
#
#     def __init__(self, **kwargs):
#         super(MainApp, self).__init__(**kwargs)
#         Settings()
#
#         self.shoes = ShoeStore()
#         if not self.shoes.shoe_list:
#             self.change_setting('selected_shoe', "No shoe selected")
#
#     def on_start(self):
#         self.setup_data_table()
#
#     def show_add_shoe_dialog(self, *args):
#         dialog = MDDialog(
#             title="Add shoe:",
#             type="custom",
#             content_cls=DialogContentAddShoe(),
#             buttons=[
#                 MDFlatButton(
#                     text="Cancel",
#                     text_color=self.theme_cls.primary_color,
#                     on_release=lambda x: dialog.dismiss()
#                 ),
#                 MDFlatButton(
#                     text="Add",
#                     text_color=self.theme_cls.primary_color,
#                     on_release=lambda x: (self.shoes.add_shoe(name=dialog.content_cls.ids.shoe_name.text),
#                                           self._change_shoe_button(dialog.content_cls.ids.shoe_name.text),
#                                           dialog.dismiss(), self.update_data_table())
#                 ),
#             ],
#         )
#         dialog.open()
#
#     def show_add_distance_dialog(self):
#         dialog = None
#         if not self.get_setting('selected_shoe') or self.get_setting('selected_shoe') == "No shoe selected":
#             dialog = MDDialog(
#                 text="No shoes, please add one :)",
#                 buttons=[
#                     MDFlatButton(
#                         text="Cancel",
#                         text_color=self.theme_cls.primary_color,
#                         on_release=lambda x: dialog.dismiss()
#                     ),
#                     MDFlatButton(
#                         text="Add shoe",
#                         text_color=self.theme_cls.primary_color,
#                         on_release=lambda x: (dialog.dismiss(), self.show_add_shoe_dialog())
#                     ),
#                 ],
#             )
#         else:
#             dialog = MDDialog(
#                 title="Add distance to {}".format(self.get_setting('selected_shoe')),
#                 type="custom",
#                 content_cls=DialogContentAddDistance(),
#                 buttons=[
#                     MDFlatButton(
#                         text="Cancel",
#                         text_color=self.theme_cls.primary_color,
#                         on_release=lambda x: dialog.dismiss()
#                     ),
#                     MDFlatButton(
#                         text="Add",
#                         text_color=self.theme_cls.primary_color,
#                         on_release=lambda x: (self.shoes.add_run(
#                             name=self.get_setting('selected_shoe'),
#                             distance=dialog.content_cls.ids.distance_text.text,
#                             km=True if self.get_setting('selected_length_unit') == "km" else False,
#                             miles=True if self.get_setting('selected_length_unit') == "miles" else False,
#                         ), dialog.dismiss(), self.update_data_table())
#                     ),
#                 ],
#             )
#         dialog.open()
#
#     def open_shoe_menu(self):
#         menu = None
#         menu_list = [{
#             "text": "Add new shoe",
#             "viewclass": "IconListItem",
#             "icon": "plus-circle-outline",
#             "on_release": lambda x=True: (self.show_add_shoe_dialog(x), menu.dismiss())}]
#         menu_list = menu_list + [{
#                 "text": shoe_name,
#                 "viewclass": "IconListItem",
#                 "icon": "shoe-sneaker",
#                 "on_release": lambda x=shoe_name: (self._change_shoe_button(x), menu.dismiss()),
#             } for shoe_name in self.shoes.shoe_list]
#         menu = MDDropdownMenu(
#             caller=self.root.ids.screen_manager.mainwin.ids.shoe_drop_item,
#             items=menu_list,
#             width_mult=4,
#         )
#         menu.bind()
#         menu.open()
#
#     def setup_data_table(self):
#         """
#         ("[size=10]Shoe Name[/size]", dp(30)),
#         """
#         self.data_table = MDDataTable(
#             size_hint=(1, .93),
#             use_pagination=False,
#             rows_num=20,
#             check=False,
#             column_data=[
#                 ("", dp(1)),
#                 ("Name", dp(30)),
#                 ("Runs", dp(10)),
#                 ("Km", dp(12)),
#                 # ("Miles", dp(12)),
#                 ("Added", dp(20)),
#                 # ("Status", dp(10))
#             ],
#             row_data=self.shoes.table_data,
#             sorted_on="Name",
#             # sorted_order="ASC",
#             elevation=2
#         )
#         self.data_table.bind(on_row_press=self.on_row_press)
#         self.data_table.bind(on_check_press=self.on_check_press)
#
#         self.root.ids.screen_manager.statswin.ids.stats_table.add_widget(self.data_table)
#
#     def update_data_table(self):
#         self.data_table.row_data = self.shoes.table_data
#
#     def _change_shoe_button(self, name):
#         self.root.ids.screen_manager.mainwin.ids.shoe_drop_item.text = name
#         self.change_setting('selected_shoe', name)
#
#     def switch_to_screen(self, screen_name):
#         self.root.ids.screen_manager.current = screen_name
#
#     def on_row_press(self, instance_table, instance_row):
#         print(instance_table, instance_row)
#
#     def on_check_press(self, instance_table, current_row):
#         print(instance_table, current_row)
#
#     @staticmethod
#     def get_setting(key):
#         return Settings.get_setting(key)
#
#     @staticmethod
#     def change_setting(key, value):
#         return Settings.save_setting(key, value)
#
#     def _print(self, *args):
#         print(args)
#
#
# MainApp().run()
