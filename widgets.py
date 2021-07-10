"""
Created on 2021-07-08 16:38
@author: johannes
"""
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineListItem, OneLineIconListItem, MDList
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.datatables import MDDataTable
from kivy.clock import Clock


class DialogContentAddDistance(BoxLayout):
    pass


class DialogContentAddShoe(BoxLayout):
    pass


class ContentNavigationDrawer(BoxLayout):
    pass


class DrawerList(ThemableBehavior, MDList):
    pass


class AppToolbar(MDToolbar):
    def __init__(self, **kw):
        super(AppToolbar, self).__init__(**kw)
        Clock.schedule_once(self.set_toolbar_font_size)

    def set_toolbar_font_size(self, *args):
        self.ids.label_title.font_size = '12sp'


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class IconListItem(OneLineIconListItem):
    icon = StringProperty()
