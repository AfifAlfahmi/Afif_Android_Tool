import os
import time
from pathlib import Path

from kivy.uix.widget import Widget
from kivy.lang import Builder
from plyer import filechooser

from src.logs_patch import logFunName
from src.manifest_parser import getPackageName, openManifest
from src.patch_apk import patchManifestDebuggable
from src.python.Certificate import Certificate
from src.python.Dynamic import Dynamic
from src.python.Sidebar import Sidebar
from src.python.Sign import Sign
from src.python.Patch import Patch
from src.signer_script import generateCert, signApk, decompileApk, getApkDestinationFolder, buildApk, buildApk, \
    decompileApk, zipAlignApk
from kivy.clock import Clock

from threading import Thread
from time import sleep

Builder.load_file("../kivy_layouts/apk.kv")

class Apk(Widget):

    certLayOutDidplayed = False
    signLayoutDisplayed = True
    patchLayoutDisplayed = False
    dynamicLayoutDisplayed = False
    logFunctions = True
    isPatched = False
    isBuilt = False
    interval = None



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
        self.uploadApkAnylBtn = self.dynamic.ids.uploadApkAnylBtn

        self.debugApkBtn = self.patchLayout.ids.debugApkBtn
        self.log_funs_check_box = self.patchLayout.ids.log_funs_check_box
        self.log_funs_label = self.patchLayout.ids.log_funs_label
        self.progressBar = self.patchLayout.ids.patch_progress_bar
        self.progressLabel = self.patchLayout.ids.progress_label


        self.signBtn.bind(on_press=lambda y: self.toSign())
        self.patchBtn.bind(on_press=lambda y: self.toPatch())
        self.dynamicBtn.bind(on_press=lambda y: self.toDynamic())
        self.uploadApkBtn.bind(on_press=lambda f:self.uploadApk("sign"))
        self.selCertBtn.bind(on_press=lambda g:self.uploadCert())
        self.newCertBtn.bind(on_press= lambda i:self.toCert())
        self.uploadApkPatchBtn.bind(on_press=lambda y: self.uploadApk("patch"))
        self.uploadApkAnylBtn.bind(on_press=lambda k: self.uploadApk("analysis"))
        self.debugApkBtn.bind(on_press=lambda m: self.operationsSchedule())
        self.log_funs_check_box.bind(active=self.on_checkbox_active)



    def uploadApk(self,type):
        print("start uploadApk fun")


        filechooser.open_file(on_selection=self.fileSelected)
        print("After file extracted")
        selectedFile = Path(self.selectedApk)
        if type == "sign":

           self.signLayout.apk_path_et.text = selectedFile.name
           self.signLayout.apkFilePath = self.selectedApk
           print("sign")

        elif type == "patch":
           self.patchLayout.apk_path_et.text = selectedFile.name
           print("patch")
        else:
            self.dynamic.apk_path_anyl_et.text = selectedFile.name
            self.dynamic.apkFilePath = self.selectedApk



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
                self.decompileApkBtn.opacity = 0
                self.log_funs_label.opacity = 1
                self.log_funs_check_box.opacity = 1
                self.debugApkBtn.opacity = 1
    def on_checkbox_active(self,checkbox, value):
        if value == True:
            print(f'check box checked {checkbox.text}')
            self.logFunctions = True

        else:
            print('check box unchecked')
            self.logFunctions = False

    def threaded_function(self,arg):


        print("thread running")
        print(f"unzipped apk {decompileApk(self.selectedApk, True)}")

        # wait 1 sec in between each thread
    def operationsSchedule(self):

        if not self.selectedApk == "":
            self.progressBar.value = 0
            self.progressBar.opacity = 1

            # self.add_widget(self.pb)

            print(f"before decompile ")



            print(f"unzipped apk {decompileApk(self.selectedApk, True)}")
            self.progressLabel.text = "decompiling..."
            # thread = Thread(target=self.threaded_function, args=(10,))
            # thread.start()
            # thread.join()
            # print("thread finished...exiting")
            self.interval = Clock.schedule_interval(self.next, 1)

        else:
            self.progressLabel.text = "Apk not selected"







    def patchApkOptions(self):

        #projectPath = Path(srcDir/"deb_tool")
        projectPath = getApkDestinationFolder(self.selectedApk)
        packageName = getPackageName(self,openManifest(self,projectPath))
        print(f"getPackage name {packageName}")

        if self.logFunctions:
            logFunName(projectPath, packageName)
            patchManifestDebuggable(openManifest(self,projectPath))
        # else:
        #
        #     patchManifestDebuggable()
        self.isPatched = True

    def next(self, dt):
        value = self.progressBar.value
        if value < 100:

            self.progressBar.value += 5
        if value == 100 and not self.isPatched:
            self.progressLabel.text = "patching..."
            self.progressBar.value = 0
            self.patchApkOptions()

        if self.progressBar.value == 60 and self.isPatched and not self.isBuilt:
            self.progressLabel.text = "building.."
            self.progressBar.value = 0
            projectPath = getApkDestinationFolder(self.selectedApk)
            buildApk(projectPath)
            self.isBuilt = True
        if self.progressBar.value == 90 and   self.isBuilt and self.isPatched:
            time.sleep(2)
            zipAlignApk(self.selectedApk)
            self.interval.cancel()
            self.progressBar.opacity = 0
            self.progressLabel.text = "Done"


            # self.ids.my_label.text = f'{int(self.pb.value)}% Progress'


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