
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from plyer import filechooser

from src.patch_apk import patchManifestDebuggable
from src.python.Certificate import Certificate
from src.python.Sidebar import Sidebar
from src.python.Sign import Sign
from src.python.Patch import Patch

from src.signer_script import generateCert, signApk, unzipApk

Builder.load_file("../kivy_layouts/apk.kv")

class Apk(Widget):

    certLayOutDidplayed = True
    signLayoutDisplayed = False
    patchLayoutDisplayed = False

    selectedApk = ""



    def __init__(self, **kwargs):
        super(Apk, self).__init__(**kwargs)
        self.apkLayout = self.ids.apkLayout
        self.certLayout = Certificate()
        self.signLayout = Sign()
        self.patchLayout = Patch()

        self.sidebar = Sidebar()

        self.apkLayout.add_widget(self.signLayout)
        self.apkLayout.add_widget(self.certLayout)
        self.apkLayout.add_widget(self.patchLayout)

        self.apkLayout.add_widget(self.sidebar)
        self.certBtn = self.sidebar.ids.certBtn
        self.signBtn = self.sidebar.ids.signBtn
        self.patchBtn = self.sidebar.ids.patchBtn

        self.uploadApkBtn = self.signLayout.ids.uploadApkBtn
        self.selCertBtn = self.signLayout.ids.selCertBtn
        self.createCertBtn = self.certLayout.ids.creCertBtn
        self.signApkBtn = self.signLayout.ids.signApkBtn
        self.testSignChBox = self.signLayout.ids.testSignChBox
        self.prodSignChBox = self.signLayout.ids.prodSignChBox
        self.prodSignLayout = self.signLayout.ids.prodSignLayout

        self.uploadApkPatchBtn = self.patchLayout.ids.uploadApkBtn
        self.debugApkBtn = self.patchLayout.ids.debugApkBtn


        self.certBtn.bind(on_press=lambda x: self.toCert())
        self.signBtn.bind(on_press=lambda y: self.toSign())
        self.patchBtn.bind(on_press=lambda y: self.toPatch())

        self.createCertBtn.bind(on_press=lambda z: self.createCertificate())
        self.uploadApkBtn.bind(on_press=lambda f:self.uploadApk(True))
        self.selCertBtn.bind(on_press=lambda g:self.uploadCert())
        self.signApkBtn.bind(on_press= lambda h:self.signApkValidation())
        self.testSignChBox.bind(active=self.on_checkbox_Active)
        self.prodSignChBox.bind(active= self.on_checkbox_Active)

        self.uploadApkPatchBtn.bind(on_press=lambda y: self.uploadApk(False))
        self.debugApkBtn.bind(on_press=lambda m: self.makeApkDebuggable())

    def createCertificate(self):
        print("start create cert")

        outKeyFile =  self.certLayout.outKeyFile.text
        c_name = self.certLayout.c_name.text
        org = self.certLayout.org.text

        loc = self.certLayout.loc.text
        country = self.certLayout.country.text
        keyPass = self.certLayout.keyPass.text
        storePass =self.certLayout.storePass.text
        alias = self.certLayout.alias.text


        print(f"out{c_name}")
        if(alias.count(" ") > 0) or outKeyFile.count(" ") > 0:
            print(f"found space")

        elif(not outKeyFile or not c_name or not org or not loc or not country or not keyPass or not storePass or not alias):
            print(f"empty str in cert")
        else:
          generateCert(outKeyFile, c_name, "dkkfg", org, loc, "makkah",country, keyPass,
                     storePass, alias)
    def signApkValidation(self):
        print("start apk signing")
        apkPath = self.signLayout.apk_path_et.text
        keyPath = self.signLayout.keyPathET.text
        storePass = self.signLayout.signStorePass.text

        keyPass = self.signLayout.signKeyPass.text
        alias = self.signLayout.signAlias.text
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


    def showProdSignDetails(self):
            print('prod sign')
            apkPath = self.apk_path_et.text

    def prodSign(self):
        self.prodSignLayout.opacity = 1
        self.signApkBtn. pos_hint ={'center_x':.5, 'center_y':.1}


    def testSign(self):
        self.prodSignLayout.opacity = 0
        self.signApkBtn. pos_hint ={'center_x':.5, 'center_y':.5}


    def uploadApk(self,isSign):
        filechooser.open_file(on_selection=self.fileSelected)
        print("After file extracted")
        if isSign:

           self.signLayout.apk_path_et.text = self.selectedApk
           print("sign")

        else:
           self.patchLayout.apk_path_et.text = self.selectedApk
           print("patch")



    def uploadCert(self):
        filechooser.open_file(on_selection=self.fileSelected)


    def fileSelected(self, selection):

        # print(selection)
        if selection:
            if selection[0].endswith(".apk"):
                print("ext APK")

                self.selectedApk = selection[0]


            elif  selection[0].endswith(".jks") or selection[0].endswith(".KEYSTORE"):
                self.signLayout.keyPathET.text = selection[0]
                #self.signApkValidation()


            else:

                print(selection[0])


    def makeApkDebuggable(self):
        print(f"unzipped apk {unzipApk(self.selectedApk)}")
        #patchManifestDebuggable()


    def toCert(self):

        if not self.certLayOutDidplayed:
            self.apkLayout.remove_widget(self.signLayout)
            self.apkLayout.add_widget(self.certLayout)
            self.certLayOutDidplayed = True
            self.patchLayoutDisplayed = False

            self.signLayoutDisplayed = False
        self.apkLayout.remove_widget(self.sidebar)
        self.apkLayout.add_widget(self.sidebar)

    def toSign(self):

        #self.certLayout.opacity = 0
        if not self.signLayoutDisplayed:
            self.apkLayout.remove_widget(self.signLayout)
            self.apkLayout.remove_widget(self.certLayout)
            self.apkLayout.add_widget(self.signLayout)
            self.signLayout.ids.signLayout.opacity = 1
            self.signLayoutDisplayed = True
            self.patchLayoutDisplayed = False

            self.certLayOutDidplayed = False
        self.apkLayout.remove_widget(self.sidebar)
        self.apkLayout.add_widget(self.sidebar)

    def toPatch(self):

        #self.certLayout.opacity = 0
        if not self.patchLayoutDisplayed:
            self.apkLayout.remove_widget(self.signLayout)
            self.apkLayout.remove_widget(self.certLayout)
            self.apkLayout.remove_widget(self.patchLayout)

            self.apkLayout.add_widget(self.patchLayout)
            self.patchLayout.ids.patchLayout.opacity = 1
            self.patchLayoutDisplayed = True

            self.signLayoutDisplayed = False
            self.certLayOutDidplayed = False
        self.apkLayout.remove_widget(self.sidebar)
        self.apkLayout.add_widget(self.sidebar)