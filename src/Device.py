
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window

from Apps import Apps
from File import File
from Sidebar import Sidebar

Builder.load_file("kivy_layouts/device.kv")


class Device(Widget):
    appsMenuItem = "Apps"
    filesMenuItem = "Files"
    appsLayoutDidplayed = True
    fileLayoutDidplayed = False


    def __init__(self, **kwargs):
        super(Device, self).__init__(**kwargs)
        self.deviceLayout = self.ids.deviceLayout
        self.sidebar = Sidebar()

        self.file = File()

#        self.recViewLayout = self.apps.ids.recViewLayout

        self.appsBtn = self.sidebar.ids.btn1
        self.filesBtn = self.sidebar.ids.btn2
        self.sidebar.ids.btn3.opacity = 0

        self.appsBtn.text = self.appsMenuItem
        self.filesBtn.text = self.filesMenuItem

        self.apps = Apps()
        self.deviceLayout.add_widget(self.apps)
        self.apps.downLoadApps()

        window_width, window_height = Window.size

        self.deviceLayout.add_widget(self.sidebar)

        self.appsBtn.bind(on_press=lambda y: self.toAppsList())
        self.filesBtn.bind(on_press=lambda y: self.toFiles())


    def toAppsList(self):

        if not self.appsLayoutDidplayed:
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
            self.deviceLayout.remove_widget(self.apps)
            self.deviceLayout.add_widget(self.file)

            self.fileLayoutDidplayed = True
            self.appsLayoutDidplayed = False
            self.filesBtn.background_color = 1, 1, 1, 1
            self.appsBtn.background_color = 0.67, 0.67, 0.67, 1

        self.deviceLayout.remove_widget(self.sidebar)
        self.deviceLayout.add_widget(self.sidebar)



    pass





