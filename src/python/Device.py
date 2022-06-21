
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.core.window import Window

from src.adb_script import getPackages
from src.files import getApk
from src.python.Apps import Apps
from src.python.File import File
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
    appsLayoutDidplayed = True
    fileLayoutDidplayed = False


    def __init__(self, **kwargs):
        super(Device, self).__init__(**kwargs)
        self.deviceLayout = self.ids.deviceLayout
        self.sidebar = Sidebar()
        self.apps = Apps()
        self.file = File()

#        self.recViewLayout = self.apps.ids.recViewLayout

        self.appsBtn = self.sidebar.ids.btn1
        self.filesBtn = self.sidebar.ids.btn2
        self.sidebar.ids.btn3.opacity = 0


        self.appsBtn.text = self.appsMenuItem
        self.filesBtn.text = self.filesMenuItem


        self.deviceLayout.add_widget(self.apps)
        window_width, window_height = Window.size
        print(f"self width{window_width}")





        self.deviceLayout.add_widget(self.sidebar)



        self.appsBtn.bind(on_press=lambda y: self.toAppsList())
        self.filesBtn.bind(on_press=lambda y: self.toFiles())


    def toAppsList(self):
        if not self.appsLayoutDidplayed:

           print("to apps list")
           self.deviceLayout.remove_widget(self.file)
           self.deviceLayout.add_widget(self.apps)
           self.appsLayoutDidplayed = True
           self.fileLayoutDidplayed = False
           self.appsBtn.background_color = 1, 1, 1, 1
           self.filesBtn.background_color = 0.67, 0.67, 0.67, 1

        self.deviceLayout.remove_widget(self.sidebar)
        self.deviceLayout.add_widget(self.sidebar)

    def toFiles(self):
        if not self.fileLayoutDidplayed:

            print("to files")
            self.deviceLayout.remove_widget(self.apps)
            self.deviceLayout.add_widget(self.file)

            self.fileLayoutDidplayed = True
            self.appsLayoutDidplayed = False
            self.filesBtn.background_color = 1, 1, 1, 1
            self.appsBtn.background_color = 0.67, 0.67, 0.67, 1

        self.deviceLayout.remove_widget(self.sidebar)
        self.deviceLayout.add_widget(self.sidebar)





    pass





