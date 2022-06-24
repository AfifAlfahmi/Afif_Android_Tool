from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget

from src.adb_script import getPackages
from src.files import getApk
import time
from kivy.clock import Clock

Builder.load_file("../kivy_layouts/apps.kv")
from kivy.uix.button import Button

from ppadb.client import Client as AdbClient

class Apps(Widget):

    interval = None
    package = ""

    def __init__(self, **kwargs):
        super(Apps, self).__init__(**kwargs)
        self.appsGradeLayout = self.ids.appsGradeLayout
        self.extracting_label = self.ids.extracting_label
        # self.appsGradeLayout.size_hint_y = (None)
        self.appsGradeLayout.bind(minimum_height=self.appsGradeLayout.setter('height'))




    def downLoadApps(self):

        client = AdbClient(host="127.0.0.1", port=5037)
        devices = client.devices()
        if len(devices) > 0:
            device = devices[0]
            for i in getPackages(device):
                self.btn = Button(text=str(i), size_hint_y=None, size=(150, 50), )
                self.btnClone = Button(text=str("clone"), size_hint=(None, None), size=(80, 50),
                                       on_press=lambda *args, i=i: self.cloneApp(i.decode())
                                       )
                self.appsGradeLayout.add_widget(self.btn)
                self.appsGradeLayout.add_widget(self.btnClone)



    def cloneApp(self,package):
        self.extracting_label.opacity = 1
        self.extracting_label.text = "Extracting..."
        print("")
        print("")
        print("")
        print("")
        self.package = package
        self.interval = Clock.schedule_interval(self.next, 1)






    def next(self, dt):
        self.extracting_label.text = "ext..."
        getApk(self.package[8:])
        self.interval.cancel()
        self.extracting_label.text = "Done"


    pass