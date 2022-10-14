from kivy.lang import Builder
from kivy.uix.widget import Widget

from kivy.clock import Clock


Builder.load_file("kivy_layouts/apps.kv")
from kivy.uix.button import Button

from ppadb.client import Client as AdbClient
from threading import Thread
from scripts.adb_script import adb_script

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

            for i in adb_script.getPackages(device):
                self.btn = Button(text=str(i),size_hint_y=None, size=(180, 70), )

                self.btnClone = Button(text=str("Extract"), size_hint=(None, None), size=(120, 70),
                                       on_press=lambda *args, i=i: self.cloneApp(i)
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
        thread = Thread(target=adb_script.getApk, args=(self.package[8:],))
        thread.start()
        # client = AdbClient(host="127.0.0.1", port=5037)
        # devices = client.devices()
        # dev1 = devices[0]
        #
        # srcApk , destApk = getApk(self.package[8:])
        # print(f'getApp ret srcApk , destApk: {srcApk} {destApk}')
        # dev1.pull(srcApk,'C:\\Users\\Afif_Alfahmi\\PythonProjects\\Afif_Android_Tool\\workDir')
        #getApk(self.package[8:])
        self.interval.cancel()
        self.extracting_label.text = "Done"


    pass