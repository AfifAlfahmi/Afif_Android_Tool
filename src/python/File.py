import os
import time

from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget

from src.adb_script import getPackages
from src.files import getApk
from kivy.clock import Clock

Builder.load_file("../kivy_layouts/file.kv")
from kivy.uix.button import Button

from ppadb.client import Client as AdbClient
from plyer import filechooser

class File(Widget):
    selectedFile = ""
    selectedDestination = ""
    interval = None


    def __init__(self, **kwargs):
        super(File, self).__init__(**kwargs)

        self.selFileBtn = self.ids.selFileBtn
        self.pushFileBtn = self.ids.pushFileBtn
        self.spinner = self.ids.spinner
        self.push_label = self.ids.push_label


        self.selFileBtn.bind(on_press= lambda h:self.uploadFile())
        self.pushFileBtn.bind(on_press= lambda h:self.pushFile())


    def uploadFile(self):
        print("start uploadFile fun")


        filechooser.open_file(on_selection=self.fileSelected)

    def fileSelected(self, selection):

        # print(selection)
        if selection:

            self.selectedFile = selection[0]
            self.selFileBtn.text = os.path.basename(self.selectedFile)
            #self.pushFile()


    def pushFile(self):
        if self.selectedDestination == "":
            print(f"you have to select the destination path")

        else:
            print(f"selected file hi: {self.selectedFile}")
            client = AdbClient(host="127.0.0.1", port=5037)

            devices = client.devices()
            device = devices[0]
            fileName = os.path.basename(self.selectedFile)
            print(f"file name {fileName}")

            device.push(self.selectedFile, f"{self.selectedDestination}/{fileName}")
            self.push_label.text = "Done"
            self.interval = Clock.schedule_interval(self.next, 1)





    def next(self, dt):

        time.sleep(2)
        self.interval.cancel()
        self.push_label.text = ""

    def spinner_clicked(self,value):
        print(f"spinner value: {value}")
        self.selectedDestination = value

    pass