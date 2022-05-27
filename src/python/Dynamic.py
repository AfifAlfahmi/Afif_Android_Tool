from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from src.custom.FormattedLabel import FormattedLabel
from src.manifest_parser import parseManifest, getActivities, getReceivers
import os
import subprocess
from kivy.properties import ListProperty, NumericProperty
Builder.load_file("../kivy_layouts/dynamic.kv")

class Dynamic(Widget):
    def __init__(self, **kwargs):
        super(Dynamic, self).__init__(**kwargs)

        self.activitiesLayout = self.ids.activitiesLayout
        self.receiversLayout = self.ids.receiversLayout
        self.receiverLabel = self.ids.receiverLabel

        self.nameLabel = "Name"
        self.actionLabel = "Action"
        self.pencolor = ListProperty([1, 0, 0, 1])  # Red

        self.background_color = ListProperty()
        self.actNameLbl = Label(text=str("Name"), size_hint_y=None, size=(60, 15), color=(0, 0, 5, 1))
        self.actActionLbl = Label(text=str(""), size_hint_y=None, size=(60, 15), color=(0, 0, 5, 1))
        self.actEmpty = Label(text=str(""), size_hint=(None, None), size=(60, 10))
        self.actEmpty.canvas.before.add(Color(self.background_color))



        self.activitiesLayout.add_widget(self.actNameLbl)
        self.activitiesLayout.add_widget(self.actActionLbl)
        self.activitiesLayout.add_widget(self.actEmpty)





        parseManifest()
        activities =  getActivities()
        receivers = getReceivers()
        packName = parseManifest()
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
        self.recNameLbl = Label(text=str("Name"), size_hint_y=None, size=(60, 15), color=(0, 0, 5, 1))
        self.recActionLbl = Label(text=str("Action"), size_hint_y=None, size=(60, 15), color=(0, 0, 5, 1))
        self.recEmpty = Label(text=str(""), size_hint=(None, None), size=(60, 10))



        self.receiversLayout.add_widget(self.recNameLbl)
        self.receiversLayout.add_widget(self.recActionLbl)
        self.receiversLayout.add_widget(self.recEmpty)

        self.receiversLayout.bind(height=self.receiversLayout.setter('height'))

        for i in receivers:
            self.sendBtn = Button(text=str("send"), size_hint=(None,None), size=(60, 30),
                                 on_press=lambda *args, i=i: self.sendBroadCastReceiver(packName, i.name))
            self.name = Label(text=str(i.name), size_hint_y=None, size=(60, 35), color=(0, 0, 5, 1))
            self.action = Label(text=str(i.action), size_hint_y=None, size=(60, 35), color=(0, 0, 5, 1))
            self.receiversLayout.add_widget(self.name)
            self.receiversLayout.add_widget(self.action)
            self.receiversLayout.add_widget(self.sendBtn)

            #self.actBtn

            print(f"ret pack name: {packName}")

    def startActivity(self,packName,actName):
        print(f"pack name in start: {packName}")

        startActivityComm = f'adb shell am start -n {packName}/.{actName}'
        print(f"adb comm {startActivityComm}")

        subprocess.Popen("adb shell", shell=True, stdout=subprocess.PIPE)
        subprocess.Popen(f"adb shell am start -n {packName}/.{actName}", shell=True, stdout=subprocess.PIPE)

    def change_color(self, *args):

        with self.canvas:
            Color(1, 1, 1, mode='hsv')
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def sendBroadCastReceiver(self,packName,recName):
        sendBroadCastComm = f'adb shell am broadcast -n com.afif.tool/.MyBroadcastReceiver -a action com.afif.tool.MY_NOTIFICATION --es foo "bar" '
        subprocess.Popen(sendBroadCastComm , shell=True, stdout=subprocess.PIPE)
        print(f"pack name in send: {packName}")


    pass