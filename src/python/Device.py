
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.core.window import Window

from src.adb_script import getPackages
from src.files import getApk
from src.python.Apps import Apps
from src.python.Sidebar import Sidebar
from kivymd.app import MDApp
from kivy.uix.recycleview import RecycleView
from kivymd.uix.list import OneLineListItem, MDList
import shutil
from ppadb.client import Client as AdbClient
from functools import partial
Builder.load_file("../kivy_layouts/device.kv")


class Device(Widget):
    appsMenuItem = "Apps"
    filesMenuItem = "Files"

    def __init__(self, **kwargs):
        super(Device, self).__init__(**kwargs)
        self.deviceLayout = self.ids.deviceLayout
        self.sidebar = Sidebar()
        self.apps = Apps()
        self.recViewLayout = self.apps.ids.recViewLayout

        self.appsBtn = self.sidebar.ids.btn1
        self.filesBtn = self.sidebar.ids.btn2

        self.appsBtn.text = self.appsMenuItem
        self.filesBtn.text = self.filesMenuItem


        self.deviceLayout.add_widget(self.apps)
        window_width, window_height = Window.size
        print(f"self width{window_width}")





        self.deviceLayout.add_widget(self.sidebar)



        self.appsBtn.bind(on_press=lambda y: self.toAppsList())


    def toAppsList(self):
        print("to apps list")




    pass





