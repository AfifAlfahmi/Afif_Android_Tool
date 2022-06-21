
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
    signResult = ""

    def __init__(self, **kwargs):
        super(Sign, self).__init__(**kwargs)
        self.signApkBtn = self.ids.signApkBtn
        self.newCertBtn = self.ids.newCertBtn
        self.testSignChBox = self.ids.testSignChBox
        self.prodSignChBox = self.ids.prodSignChBox
        self.prodSignLayout = self.ids.prodSignLayout
        self.sign_res_status = self.ids.sign_res_status

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
                self.signResult = "all the fields required"
                self.sign_res_status.text = self.signResult

            else:
                self.signResult = signApk(self.apkFilePath, keyPath, storePass, keyPass, alias)
                self.sign_res_status.text = self.signResult

        else:
            if not self.apkFilePath:
                self.sign_res_status.text = "empty apk path"
            else:
                print(f'test sign selected')
                self.signResult = testSignApk(self.apkFilePath)
                self.sign_res_status.text = self.signResult

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
        self.signApkBtn.pos_hint = {'center_x': .385, 'center_y': .15}
        self.newCertBtn.pos_hint = {'center_x': .385, 'center_y': .09}
        self.isProdSign = True
        self.isTestSign = False
        self.sign_res_status.text = ""

    def testSign(self):
        self.prodSignLayout.opacity = 0
        self.signApkBtn.pos_hint = {'center_x': .385, 'center_y': .5}
        self.newCertBtn.pos_hint = {'center_x': .385, 'center_y': .44}
        self.isTestSign = True
        self.isProdSign = False
        self.sign_res_status.text = ""

    pass