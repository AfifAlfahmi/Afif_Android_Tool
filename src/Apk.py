import time
from pathlib import Path

from kivy.uix.widget import Widget
from kivy.lang import Builder

from scripts.logs_patch import logFunName
from scripts.manifest_parser import getPackageName, openManifest
from scripts.patch_apk import patchManifestDebuggable
from Certificate import Certificate
from Dynamic import Dynamic
from Sidebar import Sidebar
from Sign import Sign
from Patch import Patch

from kivy.clock import Clock
from threading import Thread
from scripts.signer_script import signer_script
import easygui

Builder.load_file("kivy_layouts/apk.kv")

class Apk(Widget):

    certLayOutDidplayed = False
    signLayoutDisplayed = True
    patchLayoutDisplayed = False
    dynamicLayoutDisplayed = False
    logFunctions = True
    inBuild = False

    interval = None



    selectedApk = ""
    selectedCert = ""

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


        #filechooser.open_file(on_selection=self.fileSelected)
        print('before calling openbox')
        selectedFile = easygui.fileopenbox(msg="Choose a file",default=r"C:\Users\user\.atom\*")
        print(f'after calling openbox {selectedFile}')

        self.fileSelected(selectedFile)

        if(not self.selectedApk == ""):
            self.selectedApk = Path(self.selectedApk)
            if type == "sign":
                self.signLayout.apk_path_et.text = self.selectedApk.name
                self.signLayout.apkFilePath = self.selectedApk

            elif type == "patch":
                self.patchLayout.apk_path_et.text = self.selectedApk.name

            else:
                print(f'selectedApk {self.selectedApk}')

                self.dynamic.apk_path_anyl_et.text = self.selectedApk.name
                self.dynamic.apkFilePath = self.selectedApk






    def uploadCert(self):
        selectedFile = easygui.fileopenbox(msg="Choose a file", default=r"C:\Users\user\.atom\*")
        self.fileSelected(selectedFile)


    def fileSelected(self, selection):

        # print(selection)
        self.signLayout.sign_res_status.text = ""
        if selection:
            if selection.endswith(".apk"):
                self.selectedApk = selection

            elif  selection.endswith(".jks") or selection.endswith(".KEYSTORE") or selection.endswith(".keystore"):
                self.selectedCert = Path(selection)
                self.signLayout.keyPathET.text = self.selectedCert.name
                self.signLayout.certFilePath = self.selectedCert
                #self.signApkValidation()
            else:
                print(f'file extension not supported  {selection}')
                # self.decompileApkBtn.opacity = 0
                # self.log_funs_label.opacity = 1
                # self.log_funs_check_box.opacity = 1
                # self.debugApkBtn.opacity = 1


    def on_checkbox_active(self,checkbox, value):
        if value == True:
            self.logFunctions = True

        else:
            self.logFunctions = False

    def threaded_function(self,arg):
        print(f"unzipped apk")

        # wait 1 sec in between each thread
    def operationsSchedule(self):

        if not self.selectedApk == "":
            self.progressBar.value = 0
            self.progressBar.opacity = 1
            thread = Thread(target=signer_script.decompileApk, args=(signer_script,self.selectedApk,True,))
            thread.start()
            #print(f"{decompileApk(self.selectedApk, True)}")
            self.progressLabel.text = "decompiling..."
            # thread = Thread(target=self.threaded_function, args=(10,))
            # thread.start()
            # thread.join()
            # print("thread finished...exiting")
            self.interval = Clock.schedule_interval(self.next,1)

        else:
            self.progressLabel.text = "Apk not selected"







    def patchApkOptions(self):

        #projectPath = Path(srcDir/"deb_tool")
        projectPath = signer_script.getApkDestinationFolder(self.selectedApk)
        packageName = getPackageName(self,openManifest(self,projectPath))

        if self.logFunctions:
            logFunName(projectPath, packageName)
            patchManifestDebuggable(openManifest(self,projectPath))

        signer_script.isPatched = True

    def next(self, dt):
        value = self.progressBar.value
        if value < 100 :
            self.progressBar.value += 5

        if  signer_script.isDecompiled and not signer_script.isPatched:
            print('decompiled seccucfly')
            self.progressLabel.text = "patching..."
            self.progressBar.value = 0
            self.patchApkOptions()


        # if value == 100 and not signer_script.isPatched:
        #     self.progressLabel.text = "patching..."
        #     self.progressBar.value = 0
        #     self.patchApkOptions()

        if signer_script.isPatched and not signer_script.isBuilt and not self.inBuild and self.progressBar.value >= 40:
            self.progressLabel.text = "building..."
            self.progressBar.value = 0
            projectPath = signer_script.getApkDestinationFolder(self.selectedApk)
            thread = Thread(target=signer_script.buildApk,args=(signer_script,projectPath,))
            thread.start()
            #buildApk(projectPath)
            #signer_script.isBuilt = True
            self.inBuild = True
        if  signer_script.isBuilt and signer_script.isPatched:
            time.sleep(1)
            # zipAlignApk(self.selectedApk)
            self.interval.cancel()
            self.progressBar.opacity = 0
            self.progressLabel.text = "Done"


            # self.ids.my_label.text = f'{int(self.pb.value)}% Progress'


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
            self.signBtn.background_color = 1, 1, 1, 1
            self.patchBtn.background_color = 0.67, 0.67, 0.67, 1
            self.dynamicBtn.background_color = 0.67, 0.67, 0.67, 1


        self.apkLayout.remove_widget(self.sidebar)
        self.apkLayout.add_widget(self.sidebar)

    def toPatch(self):

        #self.certLayout.opacity = 0
        if not self.patchLayoutDisplayed:
            self.apkLayout.remove_widget(self.signLayout)
            self.apkLayout.remove_widget(self.certLayout)
            self.apkLayout.remove_widget(self.patchLayout)
            self.apkLayout.remove_widget(self.dynamic)
            self.patchBtn.background_color = 1, 1, 1, 1
            self.signBtn.background_color = 0.67, 0.67, 0.67, 1
            self.dynamicBtn.background_color = 0.67, 0.67, 0.67, 1



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
            self.dynamicBtn.background_color = 1, 1, 1, 1
            self.signBtn.background_color = 0.67, 0.67, 0.67, 1
            self.patchBtn.background_color = 0.67, 0.67, 0.67, 1
        self.apkLayout.remove_widget(self.sidebar)
        self.apkLayout.add_widget(self.sidebar)