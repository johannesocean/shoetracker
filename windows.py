"""
Created on 2021-07-07 17:27
@author: johannes
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


class RootWindow(Screen):
    mainwin = ObjectProperty()


class MainWindow(Screen):
    pass


class StatsWindow(Screen):
    pass
