import shutil
import subprocess
import os



ADB = shutil.which("adb")

out = os.popen('adb shell "dumpsys activity | grep "MainActivity""').read() #os.popen support for read operations
print(out)
packageName = "com.example.nativeandroidapp"

def getApk(packageName):
  getPathComm = 'adb shell pm path'
  pathReq = subprocess.Popen(f'{getPathComm} {packageName}', shell=True, stdout=subprocess.PIPE)
  resultBytes = pathReq.stdout.read()
  resultStr = resultBytes.decode("utf-8")
  pathRes = resultStr[8:]
  tupleResult = pathReq.communicate()
  splitedPath = tupleResult[0].splitlines()

  subprocess.Popen(f'adb pull {pathRes}', shell=True, stdout=subprocess.PIPE)
  print(f'result of str {resultStr}')
  print(f'path of result: {pathRes}')
  print(f'type of str {type(resultStr)}')


getApk(packageName)

