"""
Created on 2021-07-07 17:14
@author: johannes
"""
import flet as ft
from shoe import DataHandler
from utils import get_base64


TABLE_COLUMNS = {
    "Name": "name",
    "Runs": "number_of_runs",
    "Km": "accumulated_distance_km",
    "Added": "time_of_creation"
}


def main(page: ft.Page):
    page.title = "Shoetracker"
    data_handler = DataHandler(page)

    def get_distance_dialog_title():
        return ft.Text(f"Add distance to {data_handler.get_selected_shoe()}")

    def get_table_rows():
        def get_cell_content(attr, shoe):
            if attr == "name":
                return ft.Row(
                    [ft.Icon(name="check_circle", color="green"), ft.Text(shoe.get(attr), color="black")],
                    alignment=ft.MainAxisAlignment.START
                )
            else:
                return ft.Text(shoe.get(attr), color="black")
        shoes = data_handler.get_all_shoes()
        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(get_cell_content(attr, shoe))
                    for attr in TABLE_COLUMNS.values()
                ],
            ) for shoe in shoes.values()
        ]

    def layout_change(page_name):
        page.controls = []
        if page_name == "home":
            add_item(home_page)
        elif page_name == "statistic":
            data_table.rows = get_table_rows()
            add_item(stats_page)
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
        distance_dlg_modal.title = get_distance_dialog_title()
        page.dialog = distance_dlg_modal
        distance_dlg_modal.open = True
        page.update()

    def add_distance_dlg(e):
        if distance_text.value:
            data_handler.add_distance_to_shoe(shoes_dropdown.value,
                                              distance=distance_text.value)
            distance_text.value = ""
        distance_dlg_modal.open = False
        page.update()

    def on_dropdown_change(e):
        data_handler.set_selected_shoe(shoes_dropdown.value)
        distance_dlg_modal.title = ft.Text(f"Add distance to {shoes_dropdown.value or ''}")

    new_shoe_text = ft.TextField(helper_text="Example: Sense Ride 4")
    dlg_modal = ft.AlertDialog(modal=True,
                               title=ft.Text("Add new shoe"),
                               content=new_shoe_text,
                               actions=[ft.TextButton("Add", on_click=add_and_close_dlg),
                                        ft.TextButton("Cancel", on_click=close_dlg)],
                               actions_alignment=ft.MainAxisAlignment.END)
    shoes_dropdown = ft.Dropdown(options=[ft.dropdown.Option(_shoe) for _shoe in data_handler.get_shoe_list()],
                                 value=data_handler.get_selected_shoe(),
                                 width=200,
                                 on_change=on_dropdown_change,
                                 filled=True,
                                 color="black",
                                 bgcolor="white",
                                 focused_color="black",
                                 focused_bgcolor="white")
    add_shoe_button = ft.ElevatedButton("Add",
                                        icon=ft.icons.ADD_CIRCLE_ROUNDED,
                                        icon_color="green400",
                                        on_click=open_dlg_modal)

    distance_text = ft.TextField(helper_text="Km - Example: 17.3")
    distance_dlg_modal = ft.AlertDialog(modal=True,
                                        title=get_distance_dialog_title(),
                                        content=distance_text,
                                        actions=[ft.TextButton("Add", on_click=add_distance_dlg),
                                                 ft.TextButton("Cancel", on_click=close_dlg)],
                                        actions_alignment=ft.MainAxisAlignment.END)
    add_distance_button = ft.ElevatedButton("Add distance to shoe!",
                                            icon=ft.icons.RUN_CIRCLE_ROUNDED,
                                            icon_color="green400",
                                            on_click=open_distance_dlg_modal)
    app_bar = ft.Row([ft.IconButton(ft.icons.BAR_CHART_SHARP, on_click=lambda _: layout_change("statistic")),
                      ft.IconButton(ft.icons.HOME_SHARP, on_click=lambda _: layout_change("home"))],
                     alignment=ft.MainAxisAlignment.END)
    home_page = ft.Container(
        image_src_base64=get_base64("assets/jogging.png"),
        image_fit=ft.ImageFit.COVER,
        expand=True,
        content=ft.Column(
            [
                app_bar,
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
    )
    data_table = ft.DataTable(columns=[ft.DataColumn(ft.Text(col, color="black"), numeric=True if col in {"Runs", "Km"} else False)
                                       for col in TABLE_COLUMNS],
                              rows=get_table_rows(),
                              expand=True,
                              column_spacing=50,
                              divider_thickness=0,
                              bgcolor="white")
    stats_page = ft.Container(image_src_base64=get_base64("assets/jogging.png"),
                              image_fit=ft.ImageFit.COVER,
                              expand=True,
                              content=ft.Column([app_bar, ft.Row([data_table], alignment=ft.MainAxisAlignment.CENTER)]),
                              alignment=ft.alignment.top_center)

    add_item(home_page)


ft.app(
    port=8080,
    target=main,
    assets_dir="assets",
    view=ft.WEB_BROWSER
)
