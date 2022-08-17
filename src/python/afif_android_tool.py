from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from plyer import filechooser

# class MainWindow(Screen):
#     root = Widget()
#     root.add_widget(Button())
#     slider = Slider()
#     root.add_widget(slider)
from src.python.Apk import Apk
from src.python.Certificate import Certificate
from src.python.Sidebar import Sidebar
from src.python.Sign import Sign
from src.signer_script import *
import types
class WindowManager(ScreenManager):
    pass


class HomeScreen(Screen):
    isDeviceLayoutDispalyed = False


    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.box_layout = BoxLayout()
        self.nav = Navbar()
        self.apk = Apk()

        self.box_layout.add_widget(
            Label(text="Afif Grid"))
        # self.add_widget(self.box_layout)
        self.add_widget(self.nav)
        self.add_widget(self.apk)
        self.toDeviceBtn = self.nav.ids.devbtn
        self.toApkBtn = self.nav.ids.apkbtn
        self.toDeviceBtn.bind(on_press=lambda x: self.toDevice())
        self.toApkBtn.bind(on_press=lambda x: self.toApk())

    def toDevice(self):

        from src.python.Device import Device
        self.device = Device()
        self.remove_widget(self.apk)
        self.remove_widget(self.device)

        self.add_widget(self.device)
        self.isDeviceLayoutDispalyed = True
        self.toDeviceBtn.background_color = 1, 1, 1, 1
        self.toApkBtn.background_color = 0.67, 0.67, 0.67, 1
        #self.toDeviceBtn.background_color = 0.89, 0.89, 0.89, 1
        #self.toDeviceBtn.background_color = 0.96, 0.99, 0.99, 1


    def toApk(self):
        if self.isDeviceLayoutDispalyed:
            self.toApkBtn.background_color = 1, 1, 1, 1
            self.toDeviceBtn.background_color = 0.67, 0.67, 0.67, 1
            self.remove_widget(self.device)
            self.remove_widget(self.apk)
            self.add_widget(self.apk)


Builder.load_file("../kivy_layouts/navbar.kv")


class Navbar(Widget):

    pass


class SecondScreen(Screen):
    pass


kv = Builder.load_file('../kivy_layouts/home.kv')

class NavApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    NavApp().run()
