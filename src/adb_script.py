
import shutil
import subprocess
import tempfile
import os


from ppadb.client import Client as AdbClient

ADB = shutil.which("adb")

apk = "nat_rel_signed.apk"

adbDevsComm = 'adb devices'  # Get connected device

# subprocess.call(adbDevsComm,shell=True)
#
# out = os.popen('adb shell "dumpsys activity | grep "MainActivity""').read() #os.popen support for read operations
# print(out)


client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()


def isAppInstalled(device, package):
    isInstalled = device.is_installed(package)

    return isInstalled

def pushFile(device,src,dest):
    device.push(src,dest)
    #device.push("adb_push.txt", "/sdcard/Download/afif.txt")

def pullFile(device,src,dest):
    device.pull(src,dest)
    # device.pull("/sdcard/Download/geo_key.jks", "pull.jks")

def installApk(device,apk):
    device.install(apk)

def unInstallApk(device,apk):
    device.install(apk)

def screenCap(device,dest):
    #result = device.screencap()
    scrCapComm = 'screencap -p'
    device.shell(f'{scrCapComm} {dest}')

def getPackages(device):
    getAppsPacksComm = "adb shell pm list packages"
    procPackages = subprocess.Popen(getAppsPacksComm, shell=True, stdout=subprocess.PIPE)
    packages = procPackages.communicate()
    splitedPackges = packages[0].splitlines()
    return splitedPackges



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



