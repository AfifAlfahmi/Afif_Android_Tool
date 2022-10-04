import time
import zipfile
import shutil
import subprocess
import tempfile
import os
import pathlib
from os.path import exists
from pathlib import Path
import sys
from threading import Thread

class signer_script :
 def __init__(self):
     print('self')



 isDecompiled = False
 isPatched = False
 isBuilt = False

 def signApkTest(apk):
     result = ""
     orgUnit = "learning"
     org = "UQU"
     location = "makkah"
     state = "makkah"
     country = "sa"
     keyPass = "wr4k_fmwlgdf"
     storePass = "xd8j42k_gskl"
     script = os.path.dirname(__file__)
     homeDir = Path(script).parent.parent.absolute()
     keyPath = Path(homeDir / "workDir/certs/test_cert.jks")

     alias = "alias1"
     apk_sign_comm = ""
     osName = sys.platform

     if osName.startswith('win'):
         whichApksigner = shutil.which("apksigner")
         if not whichApksigner:
             print('you have to download apksigner and add it to the Environment Variables ')

         apk_sign_comm = f"apksigner.bat sign --v2-signing-enabled --ks {keyPath} --ks-key-alias {alias} --ks-pass pass:{storePass} --key-pass pass:{keyPass} {apk}"

     else:
         currScript = os.path.dirname(__file__)
         homeDir = Path(currScript).parent.absolute()

         whichApksigner = shutil.which("apksigner")
         if not whichApksigner:
             whichApksigner = shutil.which("/usr/bin/apksigner")
             if not whichApksigner:
                 print('you have to download apksigner and add it to the Environment path ')

         apk_sign_comm = [
             whichApksigner,
             "sign", "--v2-signing-enabled",
             "--ks", keyPath,
             "--ks-key-alias", alias,
             "--ks-pass", 'pass:' + storePass,
             "--key-pass", 'pass:' + keyPass,
             apk
         ]

     p = subprocess.run(apk_sign_comm, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, check=False)
     if p.returncode > 0:
         stdOut = p.stdout.decode("utf8")
         print(stdOut)

         if stdOut.__contains__('Password verification failed'):
             result = 'Password verification failed'

         if stdOut.__contains__('system cannot find the file specified'):
             result = 'the system cannot find the file specified'

         else:
             result = "error, Verify the parameters values "

     else:
         result = "Apk signed successfully"

     return result

 def signApkProd(apk, keyPath, storePass, keyPass, alias):
     result = ""
     apk_sign_comm = ""
     osName = sys.platform

     if osName.startswith('win'):

         whichApksigner = shutil.which("apksigner")
         if not whichApksigner:
             print('you have to download apksigner and add it to the Environment Variables ')

         apk_sign_comm = f"apksigner.bat sign --v2-signing-enabled --ks {keyPath} --ks-key-alias {alias} --ks-pass pass:{storePass} --key-pass pass:{keyPass} {apk}"

     else:
         currScript = os.path.dirname(__file__)
         homeDir = Path(currScript).parent.absolute()
         # execSigner = Path(homeDir).joinpath('src/bins/linux/apksigner')

         whichApksigner = shutil.which("apksigner")
         if not whichApksigner:
             whichApksigner = shutil.which("/usr/bin/apksigner")
             if not whichApksigner:
                 print('you have to download apksigner and add it to the Environment path ')

         apk_sign_comm = [
             'apksigner',
             "sign", "--v2-signing-enabled",
             "--ks", keyPath,
             "--ks-key-alias", alias,
             "--ks-pass", 'pass:' + storePass,
             "--key-pass", 'pass:' + keyPass,
             apk
         ]

         # parameters = ['--ks', keyPath, '--ks-key-alias', alias, '--ks-pass', 'pass:{}'.format(storePass), '--key-pass',
         #            'pass:{}'.format(keyPass)]
         # signed_apk = apk.parent.joinpath('mysigned.apk')
         # cmd = [execSigner, 'sign'] + parameters + ['--out', str(signed_apk.resolve()), str(apk.resolve())]

         # out = subprocess.run(apk_sign_comm)
         # print(f'out from signer {out}')

     p = subprocess.run(apk_sign_comm, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, check=False)
     if p.returncode > 0:
         stdOut = p.stdout.decode("utf8")
         print(stdOut)

         if stdOut.__contains__('Password verification failed'):
             result = 'Password verification failed'

         if stdOut.__contains__('system cannot find the file specified'):
             result = 'the system cannot find the file specified'

         if stdOut.__contains__(f'"{alias}" does not contain a key'):

             result = 'Cannot find a key with this alias'

         else:
             result = "error, Verify the parameters values "

     else:
         result = "Apk signed successfully"

     #
     return result


# create cert

 def generateCert(outKeyFile, CName, orgUint, org, loc, country, keyPass, storePass, alias):
     result = ""

     currScript = os.path.dirname(__file__)
     homeDir = Path(currScript).parent.parent.absolute()
     certsPath = Path(homeDir / "workDir/certs/")
     outKeyFilePath = Path(certsPath).joinpath(outKeyFile)

     osName = sys.platform
     keytoolCommand = ""

     if osName.startswith('win'):

         whichKeytool = shutil.which("keytool")
         if not whichKeytool:
             print('you have to download jdk and add jdk/bin to the Environment Variables ')

         keytoolCommand = f'keytool -genkey -v -keystore {outKeyFilePath} -dname "CN={CName}, OU={orgUint}, O={org}, L={loc}, C={country}" -keypass {keyPass} -storepass {storePass} -alias {alias} -keyalg RSA -keysize 2048 -validity 10000'

     else:
         currScript = os.path.dirname(__file__)
         homeDir = Path(currScript).parent.absolute()
         print(f'path keytool home {homeDir}')

         whichKeytool = shutil.which("keytool")
         if not whichKeytool:
             whichKeytool = shutil.which("/usr/bin/keytool")
             if not whichKeytool:
                 print('you have to download jdk and add jdk/bin to the Environment path ')

         dname = f"CN={CName}, OU={orgUint}, O={org}, L={loc}, C={country}"
         keytoolCommand = [
             whichKeytool,
             "-genkey", "-v",
             "-keystore", outKeyFilePath,
             "-dname", dname,
             "-keypass", keyPass,
             "-storepass", storePass,
             "-alias", alias,
             "-keyalg", "RSA"
             , "-keysize", "2048"
             , "-validity", "10000"
         ]

     # p = os.system(keytoolCommand)
     p = subprocess.run(keytoolCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, check=False)

     if p.returncode > 0:
         stdOut = p.stdout.decode("utf8")
         print(stdOut)
         if stdOut.__contains__('already exists'):
             result = 'alias already exists'

         if stdOut.__contains__('Keystore was tampered with, or password was incorrect'):
             result = 'Keystore was tampered with, or password was incorrect'

         else:
             result = stdOut

     else:
         result = "cert created successfully"

     return result




 ADB = shutil.which("adb")

 def decompileApk(self,apk, isPatch):

     # Unzip
     # zip_ref = zipfile.ZipFile(apk, 'r')
     apkPath = Path(apk)
     osName = sys.platform

     if osName.startswith('win'):
         print(f'os name: {osName}')

         whichApktool = shutil.which("apktool")
         if not whichApktool:
             print('you have to download Apktool and add it to the Environment Variables ')

         decomipleCommand = ""
         if isPatch:
             decomipleCommand = f'apktool.bat d {apkPath} -o {self.getApkDestinationFolder(apk)}'
         else:
             decomipleCommand = f'apktool.bat d {apkPath} -f -o {self.getApkAnylDestinationFolder(apk)}'

     else:
         currScript = os.path.dirname(__file__)
         homeDir = Path(currScript).parent.absolute()

         whichApktool = shutil.which("apktool")
         if not whichApktool:
             whichApktool = shutil.which("/usr/local/bin/apktool")
             if not whichApktool:
                 print('you have to download Apktool and add it to the Environment path ')

         if isPatch:
             decomipleCommand = [
                 whichApktool,
                 "d",
                 apkPath,
                 "-o", self.getApkDestinationFolder(apk)
             ]
         else:
             decomipleCommand = [
                 whichApktool,
                 "d",
                 apkPath,
                 "-o", self.getApkAnylDestinationFolder(apk)
             ]
     print(f'paths: {decomipleCommand}')

     try:
         p = subprocess.check_output(decomipleCommand, 512, stdin=None, stderr=None, timeout=15, shell=False)
     except:
         TimeoutExpired: print('decompiling time out expy')
         self.isDecompiled = True


     print(f'decompil finished ')

     self.isDecompiled = True

     # subprocess.call("adb devices", shell=True)

     # stdOut = p.stdout.decode("utf8")
     # print(f'decompile result {stdOut}')

     # if process.returncode != 0:
     #     print(f"returncode != 0 ")

     # zip_ref.extractall(distDir)
     # zip_ref.close()
     # zipApk(workingdir)
     # Remove old signature
     # shutil.rmtree(os.path.join(workingdir, "META-INF"))

 def getApkDestinationFolder(apk):
     apkPath = Path(apk)
     appFolder = apkPath.stem

     script = os.path.dirname(__file__)
     homeDir = Path(script).parent.parent.absolute()
     workDir = Path(homeDir / "workDir")
     destDir = Path(workDir / appFolder)
     print(f'destination folder: {destDir}')

     return destDir

 def getApkAnylDestinationFolder(apk):
     apkPath = Path(apk)
     appFolder = apkPath.stem
     script = os.path.dirname(__file__)
     homeDir = Path(script).parent.parent.absolute()
     workDir = Path(homeDir / "workDir/analysis")
     destDir = Path(workDir / appFolder)
     print(f'destination anyl folder: {destDir}')

     return destDir

 def buildApk(self,projectPath,selectedApk):

     # Zip
     # print("start APK Building")
     # shutil.make_archive("new", 'zip', appFolder)
     # shutil.move("new.zip", "nat_zipped.apk")
     osName = sys.platform
     buildCommand = ""

     if osName.startswith('win'):
         print(f'os name: {sys.platform}')

         whichApktool = shutil.which("apktool")
         if not whichApktool:
             print('you have to download Apktool and add it to the Environment Variables ')

         buildCommand = f'apktool.bat b {projectPath}'

         # process = subprocess.Popen(buildCommand, shell=True, stdout=subprocess.PIPE)


     else:

         currScript = os.path.dirname(__file__)
         homeDir = Path(currScript).parent.absolute()

         whichApktool = shutil.which("apktool")
         if not whichApktool:
             whichApktool = shutil.which("/usr/local/bin/apktool")
             if not whichApktool:
                 print('you have to download Apktool and add it to the Environment path ')

         buildCommand = [
             whichApktool,
             "b",
             projectPath
         ]
     print('build command started ')
     try:
         p = subprocess.check_output(buildCommand, 512, stdin=None, stderr=None, timeout=15, shell=False)
     except:
         TimeoutExpired: print('build time out expy')
         self.isBuilt = True

     print('build command finished ')
     self.isBuilt = True

     self.zipAlignApk(projectPath,selectedApk)


 def zipAlignApk(projectPath,selectedApk):

     # projectPath = getApkDestinationFolder(selectedApk)
     apkName = Path(selectedApk).name
     # tool - release.apk
     distFolder = Path(projectPath / "dist")
     srcApkPath = Path(distFolder / apkName)
     print(f'apk file name: {apkName}')
     alignedApkPath = Path(distFolder / f"{apkName}-aligned.apk")

     argApk = f'{srcApkPath} {alignedApkPath}'

     osName = sys.platform
     zipAlignCommand = ""

     if osName.startswith('win'):

         whichZipalign = shutil.which("zipalign")
         if not whichZipalign:
             print('you have to download zipalign and add it to the Environment Variables ')

         zipAlignCommand = f'zipalign -p -f -v 4 {argApk}'



     else:
         currScript = os.path.dirname(__file__)
         homeDir = Path(currScript).parent.absolute()

         whichZipalign = shutil.which("zipalign")
         if not whichZipalign:
             whichApktool = shutil.which("/usr/local/bin/zipalign")
             if not whichApktool:
                 print('you have to download zipalign and add it to the environment path ')

         zipAlignCommand = [
             whichZipalign, "-p",
             "-f", "-v",
             "4", srcApkPath,alignedApkPath
         ]

     for i in range(4):
         if exists(srcApkPath) and i == 3:
             print('found apk in dist')

             os.system(zipAlignCommand)
             break
         time.sleep(1)


