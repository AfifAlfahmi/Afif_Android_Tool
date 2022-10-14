from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from scripts.manifest_parser import getPackageName, getActivities, getReceivers, openManifest
import subprocess
from kivy.properties import ListProperty
from threading import Thread

from scripts.signer_script import signer_script

Builder.load_file("kivy_layouts/dynamic.kv")

class Dynamic(Widget):
    apk_path_anyl_et = ObjectProperty(None)
    apkFilePath = ""
    inAnalysis  = False
    interval = None


    def __init__(self, **kwargs):
        super(Dynamic, self).__init__(**kwargs)

        self.activitiesLayout = self.ids.activitiesLayout
        self.receiversLayout = self.ids.receiversLayout
        self.receiverLabel = self.ids.receiverLabel
        self.analBtn = self.ids.analBtn
        self.analysis_progress_bar = self.ids.analysis_progress_bar
        self.anal_progress_label = self.ids.anal_progress_label

        self.background_color = ListProperty()

        self.analBtn.bind(on_press=lambda m: self.operationsSchedule())

    def analysisApk(self):

        self.actNameLbl = Label(text=str("Name"), size_hint_y=None, size=(60, 15), color=(0, 0, 0, 1))
        self.actActionLbl = Label(text=str(""), size_hint_y=None, size=(60, 15), color=(0, 0, 5, 1))
        self.actEmpty = Label(text=str(""), size_hint=(None, None), size=(60, 10))
        self.actEmpty.canvas.before.add(Color(self.background_color))

        self.activitiesLayout.add_widget(self.actNameLbl)
        self.activitiesLayout.add_widget(self.actActionLbl)
        self.activitiesLayout.add_widget(self.actEmpty)
        projectPath = signer_script.getApkAnylDestinationFolder(self.apkFilePath)

        activities =  getActivities(self,openManifest(self,projectPath))
        receivers = getReceivers(self,openManifest(self,projectPath))
        packName = getPackageName(self,openManifest(self,projectPath))

        for i in activities:
            self.actBtn = Button(text=str("Start"), size_hint=(None,None), size=(60, 30),
                                 on_press=lambda *args, i=i: self.startActivity(packName,i.name) )
            self.nameLbl = Label(text=str(i.name), size_hint_y=None, size=(60, 35),color=(0, 0, 5, 1) )
            self.actionLbl = Label(text=str(""), size_hint_y=None, size=(60, 35), color=(0, 0, 5, 1))

            self.activitiesLayout.add_widget(self.nameLbl)
            self.activitiesLayout.add_widget(self.actionLbl)

            self.activitiesLayout.add_widget(self.actBtn)

        # with self.actionLbl.canvas.before:
        #     Color(rgba=(1,0,0,1))
        #     self.rect= Rectangle(size=(160,15),pos=(self.pos))
        colr = Color(1, 0, 0, 0.5)
        rec = Rectangle(size=(40,40), pos=self.pos)

        # self.nameLbl.canvas.before.add(colr)
        # self.nameLbl.canvas.before.add(rec)

        # self.actionLbl.canvas.before.add(Rectangle(size=(50, 50))    )
        # self.actionLbl.canvas.before.add(Color(1., 2., 0)  )

        self.recNameLbl = Label(text=str("Name"), size_hint_y=None, size=(60, 15), color=(0, 0, 0, 1))
        self.recActionLbl = Label(text=str("Action"), size_hint_y=None, size=(60, 15), color=(0, 0, 0, 1))
        self.recEmpty = Label(text=str(""), size_hint=(None, None), size=(60, 10))

        self.receiversLayout.add_widget(self.recNameLbl)
        self.receiversLayout.add_widget(self.recActionLbl)
        self.receiversLayout.add_widget(self.recEmpty)

        self.receiversLayout.bind(height=self.receiversLayout.setter('height'))

        for i in receivers:
            self.sendBtn = Button(text=str("send"), size_hint=(None,None), size=(60, 30),
                                 on_press=lambda *args, i=i: self.sendBroadCastReceiver(packName, i.name,i.action))
            self.name = Label(text=str(i.name), size_hint_y=None, size=(60, 35), color=(0, 0, 5, 1))
            self.action = Label(text=str(i.action), size_hint_y=None, size=(60, 35), color=(0, 0, 5, 1))
            self.receiversLayout.add_widget(self.name)
            self.receiversLayout.add_widget(self.action)
            self.receiversLayout.add_widget(self.sendBtn)

    def operationsSchedule(self):

        self.analysis_progress_bar.value = 0

        apkPath = self.apkFilePath

        if (apkPath == ""):
            self.anal_progress_label.text = "Apk not selected"
        else:
            # signer_script.decompileApk(signer_script,apkPath, False)
            print(f'not empty apk path {apkPath}')
            signer_script.isDecompiled = False
            thread = Thread(target=signer_script.decompileApk, args=(signer_script, apkPath, False,))
            thread.start()
            self.anal_progress_label.text = "decompiling..."
            self.interval = Clock.schedule_interval(self.next, 1)
            self.analysis_progress_bar.opacity = 1

    def next(self, dt):
        value = self.analysis_progress_bar.value

        if value < 100:
            self.analysis_progress_bar.value += 5

        if signer_script.isDecompiled and not self.inAnalysis:
            self.analysis_progress_bar.value = 0
            self.anal_progress_label.text = "analysis..."
            self.inAnalysis = True


        # if value == 100:
        #     self.isDecompiled = True
        #     self.analysis_progress_bar.value = 0
        #     self.anal_progress_label.text = "analysis..."

        if value == 30 and signer_script.isDecompiled:

            self.analysisApk()
            self.interval.cancel()
            self.analysis_progress_bar.opacity = 0
            self.anal_progress_label.text = ""

    def startActivity(self,packName,actName):

        startActivityComm = f'adb shell am start -n {packName}/.{actName}'
        subprocess.Popen("adb shell", shell=True, stdout=subprocess.PIPE)
        subprocess.Popen(startActivityComm, shell=True, stdout=subprocess.PIPE)

    def change_color(self, *args):

        with self.canvas:
            Color(1, 1, 1, mode='hsv')
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def sendBroadCastReceiver(self,packName,recName,action):
        sendBroadCastComm = f'adb shell am broadcast -n {packName}/.{recName} -a action {action} --es foo "bar" '
        subprocess.Popen(sendBroadCastComm , shell=True, stdout=subprocess.PIPE)


    pass