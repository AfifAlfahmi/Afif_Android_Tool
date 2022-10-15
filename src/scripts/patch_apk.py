import zipfile
import shutil
import subprocess
import tempfile
import os
import pathlib
import re

from ppadb.client import Client as AdbClient
    # subprocess.call(['apktool', 'd', apk, '-f'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # subprocess.call(['apktool', 'b', 'nat_rel_signed'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
     # print(pi.stdout.read())
projectName = "nat_rel_signed"

def patchManifestDebuggable(manifest):

    applicationtag = "<application"
    endApplicationtag = "</application>"
    replacedDebugValue = 'android:debuggable="false" '
    newDebugValue = ' android:debuggable="true"'
    replacedNativelibsValue = 'android:extractNativeLibs="false"'
    newNativelibsValue = ' android:extractNativeLibs="true"'
    lastAppTagSym = '>'
    temp = "temp"
    tempFile = open(temp, 'w')
    with open(manifest, 'r') as f:
        debugValueFound = False
        nativeLibsValueFound = False
        inAppTag = False
        inAppBlock = False
        for line in f:

            if line.__contains__(applicationtag):
                inAppTag = True

            if inAppTag:
                if line.__contains__( replacedDebugValue ):
                    # deb value found false
                    line = line.replace(replacedDebugValue, newDebugValue)
                    debugValueFound = True

                elif line.__contains__(newDebugValue) :
                    # elif deb value found true
                    debugValueFound = True





                if line.__contains__(replacedNativelibsValue):
                    #native value found false
                    line = line.replace(replacedNativelibsValue, newNativelibsValue)
                    nativeLibsValueFound = True

                elif  line.__contains__(newNativelibsValue):
                    # elif native value found true
                    nativeLibsValueFound = True








            if inAppTag and line.__contains__(lastAppTagSym) :

                #in last app tag
                inAppTag = False
                inAppBlock = True
                splittedLine = re.split(r'( )', line)
                lastChar = splittedLine[-1][-1]
                beforLastChar = splittedLine[-1][-2]
                lastValue = splittedLine[-1][0:-2]

                if not debugValueFound and not nativeLibsValueFound:
                    # appTag all values not found
                    line = line.replace( lastValue, lastValue + newNativelibsValue+ newDebugValue )
                    debugValueFound = True
                    nativeLibsValueFound = True


                elif not debugValueFound:
                    # debug Value not Found

                    line = line.replace( lastValue, lastValue + newDebugValue )
                    debugValueFound = True

                elif not nativeLibsValueFound:
                    # native lib Value not Found
                    line = line.replace( lastValue, lastValue + newNativelibsValue )

                    nativeLibsValueFound = True


            if line.__contains__( endApplicationtag ):
                # exit app block
                inAppBlock = False


            tempFile.write(line)
    tempFile.close()
    shutil.move( temp, manifest )


    f.close()









#patchManifestDebug(projectName)