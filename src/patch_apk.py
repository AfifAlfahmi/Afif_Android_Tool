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
                print( 'inAppTag' )

            if inAppTag:
                if line.__contains__( replacedDebugValue ):
                    print('deb value found false')
                    line = line.replace(replacedDebugValue, newDebugValue)
                    debugValueFound = True
                    print('debugTag Found')

                elif line.__contains__(newDebugValue) :
                    print('elif deb value found true')
                    debugValueFound = True





                if line.__contains__(replacedNativelibsValue):
                    print('native value found false')
                    line = line.replace(replacedNativelibsValue, newNativelibsValue)
                    nativeLibsValueFound = True

                elif  line.__contains__(newNativelibsValue):
                    print('elif native value found true')
                    nativeLibsValueFound = True








            if inAppTag and line.__contains__(lastAppTagSym) :

                inAppTag = False
                inAppBlock = True
                print('in last app tag')
                splittedLine = re.split(r'( )', line)
                lastChar = splittedLine[-1][-1]
                beforLastChar = splittedLine[-1][-2]
                lastValue = splittedLine[-1][0:-2]
                print(f'last char {splittedLine[-1][-1]}')
                print(f'last char 2 {splittedLine[-1][-2]}')

                if not debugValueFound and not nativeLibsValueFound:
                    print(f'appTag all values not found:')
                    line = line.replace( lastValue, lastValue + newNativelibsValue+ newDebugValue )
                    debugValueFound = True
                    nativeLibsValueFound = True


                elif not debugValueFound:
                    print(f'debug Value not Found:')

                    line = line.replace( lastValue, lastValue + newDebugValue )
                    print(f'replaced App tag: {line}')
                    debugValueFound = True

                elif not nativeLibsValueFound:
                    print(f'native lib Value not Found')
                    line = line.replace( lastValue, lastValue + newNativelibsValue )

                    nativeLibsValueFound = True


            if line.__contains__( endApplicationtag ):
                inAppBlock = False
                print('exit app block')
                

            tempFile.write(line)
    tempFile.close()
    shutil.move( temp, manifest )


    f.close()









#patchManifestDebug(projectName)