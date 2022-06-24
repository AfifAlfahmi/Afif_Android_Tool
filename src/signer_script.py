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
    homeDir = Path(script).parent.absolute()
    keyPath = Path(homeDir/"workDir/certs/test_cert.jks")

    alias = "alias1"
    apk_sign_comm = ""
    osName = sys.platform

    if osName.__contains__('win'):
        apk_sign_comm = f"apksigner.bat sign --v2-signing-enabled --ks {keyPath} --ks-key-alias {alias} --ks-pass pass:{storePass} --key-pass pass:{keyPass} {apk}"

    else:
        apk_sign_comm = f"apksigner sign --v2-signing-enabled --ks {keyPath} --ks-key-alias {alias} --ks-pass pass:{storePass} --key-pass pass:{keyPass} {apk}"

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

def signApkProd(apk,keyPath,storePass,keyPass,alias):
    result = ""
    apk_sign_comm = ""
    osName = sys.platform

    if osName.__contains__('win'):
        apk_sign_comm = f"apksigner.bat sign --v2-signing-enabled --ks {keyPath} --ks-key-alias {alias} --ks-pass pass:{storePass} --key-pass pass:{keyPass} {apk}"

    else:
        apk_sign_comm = f"apksigner sign --v2-signing-enabled --ks {keyPath} --ks-key-alias {alias} --ks-pass pass:{storePass} --key-pass pass:{keyPass} {apk}"

    p = subprocess.run(apk_sign_comm, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, check=False)
    if p.returncode > 0:
        stdOut = p.stdout.decode("utf8")
        print(stdOut)

        if stdOut.__contains__('Password verification failed'):
            result = 'Password verification failed'

        if stdOut.__contains__('system cannot find the file specified'):
            result = 'the system cannot find the file specified'


        if stdOut.__contains__(f'"{alias}" does not contain a key') :

            result = 'Cannot find a key with this alias'

        else:
            result = "error, Verify the parameters values "

    else:
        result = "Apk signed successfully"


    return  result


# create cert

def generateCert(outKeyFile,CName,orgUint,org,loc,country,keyPass,storePass,alias):
    result = ""
    currScript = os.path.dirname(__file__)
    homeDir = Path(currScript).parent.absolute()
    certsPath = Path(homeDir/"workDir/certs/")
    outKeyFilePath  = Path(certsPath).joinpath(outKeyFile)


    keytoolCommand = f'keytool -genkey -v -keystore {outKeyFilePath} -dname "CN={CName}, OU={orgUint}, O={org}, L={loc}, C={country}" -keypass {keyPass} -storepass {storePass} -alias {alias} -keyalg RSA -keysize 2048 -validity 10000'

    #p = os.system(keytoolCommand)
    p = subprocess.run(keytoolCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, check=False)

    if p.returncode > 0:
        stdOut = p.stdout.decode("utf8")
        print(stdOut)
        if stdOut.__contains__('already exists'):
            result = 'alias already exists'

        if stdOut.__contains__('Keystore was tampered with, or password was incorrect')  :
            result = 'Keystore was tampered with, or password was incorrect'

        else:
            result = stdOut

    else:
        result = "cert created successfully"

    return result


ADB = shutil.which("adb")


def decompileApk(apk,isPatch):

    # Unzip
    #zip_ref = zipfile.ZipFile(apk, 'r')

    apkPath = Path(apk)
    decomipleCommand = ""
    if isPatch:
        decomipleCommand = f'apktool d {apkPath} -o {getApkDestinationFolder(apk)}'
    else:
        decomipleCommand = f'apktool d {apkPath} -f -o {getApkAnylDestinationFolder(apk)}'
    # subprocess.run(decomipleCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, check=False
    process = subprocess.Popen(decomipleCommand, shell=True, stdout=subprocess.PIPE)

    # if process.returncode != 0:
    #     print(f"returncode != 0 ")
    #zip_ref.extractall(distDir)
    #zip_ref.close()
    #zipApk(workingdir)
    # Remove old signature
    #shutil.rmtree(os.path.join(workingdir, "META-INF"))

def getApkDestinationFolder(apk):
    apkPath = Path(apk)
    appFolder = apkPath.stem
    script = os.path.dirname(__file__)
    homeDir = Path(script).parent.absolute()
    workDir = Path(homeDir / "workDir")
    destDir = Path(workDir / appFolder)

    return destDir
def getApkAnylDestinationFolder(apk):
    apkPath = Path(apk)
    appFolder = apkPath.stem
    script = os.path.dirname(__file__)
    homeDir = Path(script).parent.absolute()
    workDir = Path(homeDir / "workDir/analysis")
    destDir = Path(workDir / appFolder)

    return destDir



def buildApk(appFolder):

    # Zip
    # print("start APK Building")
    # shutil.make_archive("new", 'zip', appFolder)
    # shutil.move("new.zip", "nat_zipped.apk")

    buildCommand = f'apktool b {appFolder}'

    process = subprocess.Popen(buildCommand, shell=True, stdout=subprocess.PIPE)



def zipAlignApk(selectedApk):

    projectPath = getApkDestinationFolder(selectedApk)
    apkName = Path(selectedApk).name
    distFolder = Path(projectPath/"dist")
    srcApkPath = Path(distFolder/apkName)

    alignedApkPath = Path(distFolder/"aligned.apk")
    zipAlignCommand = 'zipalign -p -f -v 4 '
    argApk = f'{srcApkPath} {alignedApkPath}'

    for i in range(4):
        if exists(srcApkPath) and i == 3:
            process = os.system( zipAlignCommand + argApk )
            break
        time.sleep(1)

