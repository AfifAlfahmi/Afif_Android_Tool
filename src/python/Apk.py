
from kivy.uix.widget import Widget
from kivy.lang import Builder
from plyer import filechooser
from src.python.Certificate import Certificate
from src.python.Dynamic import Dynamic
from src.python.Sidebar import Sidebar
from src.python.Sign import Sign
from src.python.Patch import Patch
from src.signer_script import generateCert, signApk, unzipApk

Builder.load_file("../kivy_layouts/apk.kv")

class Apk(Widget):

    certLayOutDidplayed = False
    signLayoutDisplayed = True
    patchLayoutDisplayed = False
    dynamicLayoutDisplayed = False


    selectedApk = ""

    def __init__(self, **kwargs):
        super(Apk, self).__init__(**kwargs)
        self.apkLayout = self.ids.apkLayout
        self.certLayout = Certificate()
        self.signLayout = Sign()
        self.patchLayout = Patch()
        self.sidebar = Sidebar()
        self.dynamic = Dynamic()


        self.apkLayout.add_widget(self.signLayout)
        #self.apkLayout.add_widget(self.certLayout)
        #self.apkLayout.add_widget(self.patchLayout)
        self.apkLayout.add_widget(self.sidebar)
        self.signBtn = self.sidebar.ids.btn1
        self.patchBtn = self.sidebar.ids.btn2
        self.dynamicBtn = self.sidebar.ids.btn3
        self.uploadApkBtn = self.signLayout.ids.uploadApkBtn
        self.selCertBtn = self.signLayout.ids.selCertBtn
        self.newCertBtn = self.signLayout.ids.newCertBtn
        self.uploadApkPatchBtn = self.patchLayout.ids.uploadApkBtn
        self.debugApkBtn = self.patchLayout.ids.debugApkBtn

        self.signBtn.bind(on_press=lambda y: self.toSign())
        self.patchBtn.bind(on_press=lambda y: self.toPatch())
        self.dynamicBtn.bind(on_press=lambda y: self.toDynamic())
        self.uploadApkBtn.bind(on_press=lambda f:self.uploadApk(True))
        self.selCertBtn.bind(on_press=lambda g:self.uploadCert())
        self.newCertBtn.bind(on_press= lambda i:self.toCert())
        self.uploadApkPatchBtn.bind(on_press=lambda y: self.uploadApk(False))
        self.debugApkBtn.bind(on_press=lambda m: self.makeApkDebuggable())

    def uploadApk(self,isSign):
        print("start uploadApk fun")


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
        print("start to cert")

        if not self.certLayOutDidplayed:
            print("cert layout not displayed")
            self.apkLayout.remove_widget(self.signLayout)
            self.apkLayout.add_widget(self.certLayout)
            self.certLayOutDidplayed = True
            self.patchLayoutDisplayed = False

            self.signLayoutDisplayed = False
        self.apkLayout.remove_widget(self.sidebar)
        self.apkLayout.add_widget(self.sidebar)

    def toSign(self):
        print("to sign")

        #self.certLayout.opacity = 0
        if not self.signLayoutDisplayed:
            self.apkLayout.remove_widget(self.signLayout)
            self.apkLayout.remove_widget(self.certLayout)
            self.apkLayout.remove_widget(self.dynamic)

            self.apkLayout.add_widget(self.signLayout)
            self.signLayout.ids.signLayout.opacity = 1
            self.patchLayoutDisplayed = False

            self.certLayOutDidplayed = False
            self.dynamicLayoutDisplayed = False
            self.signLayoutDisplayed = True


        self.apkLayout.remove_widget(self.sidebar)
        self.apkLayout.add_widget(self.sidebar)

    def toPatch(self):

        #self.certLayout.opacity = 0
        if not self.patchLayoutDisplayed:
            self.apkLayout.remove_widget(self.signLayout)
            self.apkLayout.remove_widget(self.certLayout)
            self.apkLayout.remove_widget(self.patchLayout)
            self.apkLayout.remove_widget(self.dynamic)


            self.apkLayout.add_widget(self.patchLayout)
            self.patchLayout.ids.patchLayout.opacity = 1

            self.signLayoutDisplayed = False
            self.certLayOutDidplayed = False
            self.dynamicLayoutDisplayed = False
            self.patchLayoutDisplayed = True


        self.apkLayout.remove_widget(self.sidebar)
        self.apkLayout.add_widget(self.sidebar)

    def toDynamic(self):

        #self.certLayout.opacity = 0
        if not self.dynamicLayoutDisplayed:
            self.apkLayout.remove_widget(self.signLayout)
            self.apkLayout.remove_widget(self.certLayout)
            self.apkLayout.remove_widget(self.patchLayout)
            self.apkLayout.add_widget(self.dynamic)
            self.patchLayout.ids.patchLayout.opacity = 1
            self.patchLayoutDisplayed = False
            self.signLayoutDisplayed = False
            self.certLayOutDidplayed = False
            self.dynamicLayoutDisplayed = True
        self.apkLayout.remove_widget(self.sidebar)
        self.apkLayout.add_widget(self.sidebar)