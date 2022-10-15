
import shutil
import subprocess
import tempfile
import os
import time
from os.path import exists
from pathlib import Path

from ppadb.client import Client as AdbClient

# ADB = shutil.which("adb")
#
# apk = "nat_rel_signed.apk"
#
# adbDevsComm = 'adb devices'  # Get connected device

# subprocess.call(adbDevsComm,shell=True)
#
# out = os.popen('adb shell "dumpsys activity | grep "MainActivity""').read() #os.popen support for read operations
# print(out)


#client = AdbClient(host="127.0.0.1", port=5037)
#devices = client.devices()

class adb_script :
 def __init__(self):
    print('')

 def isAppInstalled(device, package):
     isInstalled = device.is_installed(package)

     return isInstalled

 def pushFile(device, src, dest):
     device.push(src, dest)
     # device.push("adb_push.txt", "/sdcard/Download/afif.txt")

 def pullFile(device, src, dest):
     device.pull(src, dest)
     # device.pull("/sdcard/Download/geo_key.jks", "pull.jks")

 def installApk(device, apk):
     device.install(apk)

 def unInstallApk(device, apk):
     device.install(apk)

 def screenCap(device, dest):
     # result = device.screencap()
     scrCapComm = 'screencap -p'
     device.shell(f'{scrCapComm} {dest}')

 def getPackages(device):
     client = AdbClient(host="127.0.0.1", port=5037)
     devices = client.devices()
     dev1 = devices[0]
     procPackages = dev1.shell('pm list packages')
     procPackages = procPackages.splitlines()
     return procPackages

 def getApk(packageName):

     client = AdbClient(host="127.0.0.1", port=5037)
     devices = client.devices()
     dev1 = devices[0]
     resultStr = dev1.shell(f'pm path {packageName}')
     pathRes = resultStr[8:-1]
     currScript = os.path.dirname(__file__)
     homeDir = Path(currScript).parent.parent.absolute()
     workDir = Path(homeDir / "workDir")

     first_apk = pathRes.index('.apk')
     formattedPath = pathRes[0:first_apk + 4]
     dev1.pull(formattedPath, Path(workDir/packageName))

     for i in range(4):
         baseApkPath = Path(workDir / 'base.apk')
         destApkPath = Path(workDir / f'{packageName}.apk')
         if exists(baseApkPath):
             os.rename(baseApkPath, destApkPath)
             break

         time.sleep(1)










# for device in devices:
#     print(f'is app installed: {isAppInstalled(device,"com.example.nativeandroidapp")}')
#     #device.install(apk)
#
#     screenCap(device,'/sdcard/Download/sn.png')
#     pi = subprocess.Popen(adbDevsComm, shell=True, stdout=subprocess.PIPE)
#     print('devices: '+pi.stdout.read().decode("utf-8"))
#
#     for item in getPackages(device):
#         print("type of pack item :", type(item))
#         packStr = item.decode("utf-8")
#
#         print(packStr)
#
#     print("type of getPacks :",type(getPackages(device)))


# for device in devices:
#  device.uninstall("com.example.nativeandroidapp")



