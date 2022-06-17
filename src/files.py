import shutil
import subprocess
import os
import time
from os.path import exists
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
  workDir = f"{os.getcwd()}\workDir"
  #print(f"pull apk dir: {workDir}")
  first_apk = pathRes.index('.apk')
  formattedPath = pathRes[0:first_apk+4]
  print(f"formatted str:{formattedPath}")
  pathRes = pathRes.strip()
  pullComm = f'adb pull {formattedPath} {workDir}'
  print(f"pull command: {pullComm}")
  print(f"package name: {packageName}")


  subprocess.Popen(pullComm, shell=True, stdout=subprocess.PIPE).wait()

  for i in range(4):
    print(f'i = {i}')
    if exists(f'{workDir}\\base.apk'):
      os.rename(f'{workDir}\\base.apk', f'{workDir}\\{packageName}.apk')
    time.sleep(1)




  #print(f'result of str {resultStr}')
  #print(f'path of result: {pathRes}')
  #print(f'type of str {type(resultStr)}')


#getApk(packageName)

