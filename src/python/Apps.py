from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget

from src.adb_script import getPackages
from src.files import getApk

Builder.load_file("../kivy_layouts/apps.kv")
from kivy.uix.button import Button

from ppadb.client import Client as AdbClient

class Apps(Widget):

    def __init__(self, **kwargs):
        super(Apps, self).__init__(**kwargs)
        self.appsGradeLayout = self.ids.appsGradeLayout
        # self.appsGradeLayout.size_hint_y = (None)
        self.appsGradeLayout.bind(minimum_height=self.appsGradeLayout.setter('height'))
        client = AdbClient(host="127.0.0.1", port=5037)

        devices = client.devices()
        if len(devices) > 0:
            print("found devices")
            device = devices[0]
            for i in getPackages(device):
                self.btn = Button(text=str(i), size_hint_y=None, size=(100, 80), )
                self.btnClone = Button(text=str("clone"), size_hint=(None, None), size=(40, 80),
                                       on_press=lambda *args, i=i: self.cloneApp(i.decode())
                                       )
                self.appsGradeLayout.add_widget(self.btn)
                self.appsGradeLayout.add_widget(self.btnClone)

    def cloneApp(self,package):
        #pack = self.packages[package]
        #print(f"type of package: {type(package)}")
        #print(f"clone: {package}")

       # print(f"clone {package[8:]}")
        getApk(package[8:])






    pass