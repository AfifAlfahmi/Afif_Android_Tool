import zipfile
import shutil
import subprocess
import tempfile
import os
import pathlib

from ppadb.client import Client as AdbClient
    # subprocess.call(['apktool', 'd', apk, '-f'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # subprocess.call(['apktool', 'b', 'nat_rel_signed'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
     # print(pi.stdout.read())
projectName = "nat_rel_signed"
def patchManifestDebuggable(project):

  for path in pathlib.Path(project).iterdir():
      applicationtag = "<application"
      replacedStr = '<application android:allowBackup="true" '
      newStr = '<application android:allowBackup="true" android:debuggable="true" '
      temp = "temp"
      manifestName = projectName+"\AndroidManifest.xml"
      if path.is_file():
          print("found file")
          current_file = open(path, "r")
          print(current_file.name)
          if current_file.name == manifestName:
              print(current_file.name)
              # f = open(current_file.name, "a")
              # f.write("Patched by Afif")
              # f.close()\

              tempFile = open(temp, 'w')
              with open(current_file.name, 'r') as f:
                  for line in f:
                      if line.__contains__(applicationtag):
                          line = line.replace(replacedStr,newStr)
                      tempFile.write(line)
              tempFile.close()
              shutil.move(temp, current_file.name)

          # print(current_file.read())
          current_file.close()
#patchManifestDebug(projectName)