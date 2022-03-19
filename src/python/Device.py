
from kivy.lang import Builder
from kivy.uix.widget import Widget

from src.python.Sidebar import Sidebar

Builder.load_file("../kivy_layouts/device.kv")


class Device(Widget):
    def __init__(self, **kwargs):
        super(Device, self).__init__(**kwargs)
        self.deviceLayout = self.ids.deviceLayout
        self.sidebar = Sidebar()

        self.deviceLayout.add_widget(self.sidebar)

        self.signBtn = self.sidebar.ids.signBtn
        self.signBtn.text = "Apps List"


        self.signBtn.bind(on_press=lambda y: self.toAppsList())

    def toAppsList(self):
        print("to apps list")


    pass
