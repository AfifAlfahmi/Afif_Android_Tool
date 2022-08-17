import shutil
import subprocess
import os
import time
from os.path import exists
from pathlib import Path

ADB = shutil.which("adb")

out = os.popen('adb shell "dumpsys activity | grep "MainActivity""').read() #os.popen support for read operations
print(out)
packageName = "com.example.nativeandroidapp"

def getApk(packageName):
  getPathComm = 'adb shell pm path'
  pathReq = subprocess.Popen(f'{getPathComm} {packageName}', shell=True, stdout=subprocess.PIPE)
  resultBytes = pathReq.stdout.read()
  resultStr = resultBytes.decode("utf-8")
  pathRes = resultStr[8:-1]
  tupleResult = pathReq.communicate()
  splitedPath = tupleResult[0].splitlines()

  currScript = os.path.dirname(__file__)
  homeDir = Path(currScript).parent.absolute()
  workDir = Path(homeDir / "workDir")

  #print(f"pull apk dir: {workDir}")
  first_apk = pathRes.index('.apk')
  formattedPath = pathRes[0:first_apk+4]
  pathRes = pathRes.strip()
  pullComm = f'adb pull {formattedPath} {workDir}'
  subprocess.Popen(pullComm, shell=True, stdout=subprocess.PIPE).wait()

  for i in range(4):
    baseApkPath = Path(workDir/'base.apk')
    destApkPath = Path(workDir / f'{packageName}.apk')
    if exists(baseApkPath):
      os.rename(baseApkPath, destApkPath)
      break

    time.sleep(1)


