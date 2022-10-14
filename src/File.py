import os
import time
import sys

from plyer import filechooser

from kivy.lang import Builder
from kivy.uix.widget import Widget

from kivy.clock import Clock

Builder.load_file("kivy_layouts/file.kv")

from ppadb.client import Client as AdbClient

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
        osName = sys.platform
        if osName.startswith('win'):
            import easygui
            selectedFile = easygui.fileopenbox(msg="Choose a file", default=r"C:\Users\user\.atom\*")
            self.fileSelected(selectedFile)
        else:
            filechooser.open_file(on_selection=self.fileSelected)


    def fileSelected(self, selection):

        osName = sys.platform
        if selection:
            if not osName.startswith('win'):
                selection = selection[0]

            self.selectedFile = selection
            self.selFileBtn.text = os.path.basename(self.selectedFile)


    def pushFile(self):
        if self.selectedDestination == "":
            print(f"you have to select the destination path")

        else:
            client = AdbClient(host="127.0.0.1", port=5037)

            devices = client.devices()
            device = devices[0]
            fileName = os.path.basename(self.selectedFile)

            device.push(self.selectedFile, f"{self.selectedDestination}/{fileName}")
            self.push_label.text = "Done"
            self.interval = Clock.schedule_interval(self.next, 1)





    def next(self, dt):

        time.sleep(2)
        self.interval.cancel()
        self.push_label.text = ""

    def spinner_clicked(self,value):
        self.selectedDestination = value

    pass
