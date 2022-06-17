
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget

from src.python import Apk
from src.signer_script import signApk, testSignApk

Builder.load_file("../kivy_layouts/sign_layout.kv")

class Sign(Widget):
    keyPathET = ObjectProperty(None)
    apk_path_et = ObjectProperty(None)
    signStorePass: ObjectProperty(None)
    signAlias: ObjectProperty(None)
    signKeyPass: ObjectProperty(None)
    apkFilePath = ""
    isProdSign = True
    isTestSign = False
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
        keyPath = self.keyPathET.text
        storePass = self.signStorePass.text

        keyPass = self.signKeyPass.text
        alias = self.signAlias.text
        print(f'alias {alias}')

        if self.isProdSign:
            print(f'prod sign selected')

            if (not self.apkFilePath or not keyPath or not storePass or not keyPass or not alias):
                print(f'empty apk path {self.apkFilePath}')
            else:
                print(f'not empty apk path {self.apkFilePath}')
                # unzipApk(self.apkFilePath)
                signApk(self.apkFilePath, keyPath, storePass, keyPass, alias)

        else:
            print(f'test sign selected')
            #unzipApk(self.apkFilePath)
            testSignApk(self.apkFilePath)

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
        self.isProdSign = True
        self.isTestSign = False

    def testSign(self):
        self.prodSignLayout.opacity = 0
        self.signApkBtn.pos_hint = {'center_x': .5, 'center_y': .5}
        self.isTestSign = True
        self.isProdSign = False

    pass