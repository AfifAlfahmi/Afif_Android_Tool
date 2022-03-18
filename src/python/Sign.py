
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget

from src.signer_script import signApk

Builder.load_file("../kivy_layouts/sign_layout.kv")

class Sign(Widget):
    keyPathET = ObjectProperty(None)
    apk_path_et = ObjectProperty(None)
    signStorePass: ObjectProperty(None)
    signAlias: ObjectProperty(None)
    signKeyPass: ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Sign, self).__init__(**kwargs)
        self.signApkBtn = self.ids.signApkBtn
        self.testSignChBox = self.ids.testSignChBox
        self.prodSignChBox = self.ids.prodSignChBox
        self.prodSignLayout = self.ids.prodSignLayout







        self.signApkBtn.bind(on_press= lambda h:self.signApkValidation())

        self.testSignChBox.bind(active=self.on_checkbox_Active)
        self.prodSignChBox.bind(active=self.on_checkbox_Active)





    def signApkValidation(self):
        print("start apk signing")
        apkPath = self.apk_path_et.text
        keyPath = self.keyPathET.text
        storePass = self.signStorePass.text

        keyPass = self.signKeyPass.text
        alias = self.signAlias.text
        print(f'alias {alias}')
        if (not apkPath or not keyPath or not storePass or not keyPass or not alias):
            print(f'empty apk path {apkPath}')
        else:
            print(f'not empty apk path {apkPath}')
            #unzipApk(apkPath)
            signApk(apkPath,keyPath,storePass,keyPass,alias)

    def on_checkbox_Active(self,checkboxInstance, isActive):

        if  isActive and  self.testSignChBox.active:


            print(f'test sign {checkboxInstance}')
            self.testSign()

        elif isActive and self.prodSignChBox.active :


            print(f'prod sign {checkboxInstance}')
            self.prodSign()
        else:
             print("all unchecked")

    def prodSign(self):
        self.prodSignLayout.opacity = 1
        self.signApkBtn.pos_hint = {'center_x': .5, 'center_y': .1}

    def testSign(self):
        self.prodSignLayout.opacity = 0
        self.signApkBtn.pos_hint = {'center_x': .5, 'center_y': .5}

    pass