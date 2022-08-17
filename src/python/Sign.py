
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget

from src.python import Apk
from src.signer_script import signApkTest, signApkProd

Builder.load_file("../kivy_layouts/sign_layout.kv")

class Sign(Widget):
    keyPathET = ObjectProperty(None)
    apk_path_et = ObjectProperty(None)
    signStorePass: ObjectProperty(None)
    signAlias: ObjectProperty(None)
    signKeyPass: ObjectProperty(None)
    apkFilePath = ""
    certFilePath = ""
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
        #keyPath = self.keyPathET.text
        storePass = self.signStorePass.text
        keyPass = self.signKeyPass.text
        alias = self.signAlias.text

        if self.isProdSign:

            if (not self.apkFilePath or not self.certFilePath or not storePass or not keyPass or not alias):
                self.signResult = "all the fields required"
                self.sign_res_status.text = self.signResult

            else:
                self.signResult = signApkProd(self.apkFilePath, self.certFilePath, storePass, keyPass, alias)
                self.sign_res_status.text = self.signResult

        else:
            if not self.apkFilePath:
                self.sign_res_status.text = "empty apk path"
            else:
                self.signResult = signApkTest(self.apkFilePath)
                self.sign_res_status.text = self.signResult

    def on_checkbox_Active(self,checkboxInstance, isActive):

        if  isActive and  self.testSignChBox.active:
            self.testSign()

        elif isActive and self.prodSignChBox.active :
            self.prodSign()




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