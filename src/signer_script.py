import time
import zipfile
import shutil
import subprocess
import tempfile
import os
import pathlib
from os.path import exists
from pathlib import Path



def testSignApk(apk):
    result = ""
    cName = "Afif"
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
    print("apk signer")
    print(os.getcwd())
    apk_sign_comm = f"C:\\Users\\Afif\\python_projects\\afif_android_tool\\src\\apksigner.bat sign --v2-signing-enabled --ks {keyPath} --ks-key-alias {alias} --ks-pass pass:{storePass} --key-pass pass:{keyPass} {apk}"

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
        print(f'sign status not > 0: {p.stdout.decode("utf8")}')
        result = "Apk signed successfully"


    return result

def signApk(apk,keyPath,storePass,keyPass,alias):
    result = ""
    if 1>0:
        print("apk signer")
        print(os.getcwd())
        apk_sign_comm = f"C:\\Users\\Afif\\python_projects\\afif_android_tool\\src\\apksigner.bat sign --v2-signing-enabled --ks {keyPath} --ks-key-alias {alias} --ks-pass pass:{storePass} --key-pass pass:{keyPass} {apk}"

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



    else:

        jarSigner = shutil.which("jarsigner")

        cmd_sign = [jarSigner,  "-verbose", "-sigalg", "SHA1withRSA","-digestalg", "SHA1","-keystore", keyPath,"-storepass", storePass,
            "-keypass", keyPass,apk,  alias]  # afifalias key0

        if type(cmd_sign) is str:
            cmd = cmd_sign.split(" ")
        p = subprocess.run(cmd_sign, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, check=False)
        if p.returncode > 0:
            print(p.stdout.decode("utf8"))
           # print(p.stderr.decode("utf8"))

    return  result


# create cert
def generateCert(outKeyFile,CName,orgUint,org,loc,state,country,keyPass,storePass,alias):
    result = ""
    print(f"out from signer {CName}")


    keytoolCommand = f'keytool -genkey -v -keystore {outKeyFile} -dname "CN={CName}, OU={orgUint}, O={org}, L={loc}, S={state}, C={country}" -keypass {keyPass} -storepass {storePass} -alias {alias} -keyalg RSA -keysize 2048 -validity 10000'

    #p = os.system(keytoolCommand)
    p = subprocess.run(keytoolCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, check=False)

    if p.returncode > 0:
        stdOut = p.stdout.decode("utf8")
        print(stdOut)
        result = stdOut
    else:
        result = "cert created successfully"

    return result

ADB = shutil.which("adb")

def decompileApk(apk,isPatch):

    workingdir = tempfile.mkdtemp(suffix='apkWorkingDir')
    # Unzip
    #zip_ref = zipfile.ZipFile(apk, 'r')

    apkPath = Path(apk)
    print(f"apk path {apkPath}")
    decomipleCommand = ""
    if isPatch:
        decomipleCommand = f'apktool d {apkPath} -o {getApkDestinationFolder(apk)}'
    else:
        decomipleCommand = f'apktool d {apkPath} -f -o {getApkAnylDestinationFolder(apk)}'
    # subprocess.run(decomipleCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, check=False
    process = subprocess.Popen(decomipleCommand, shell=True, stdout=subprocess.PIPE)
    print(f"after decompile ")



    if process.returncode != 0:
        print(f"returncode != 0 ")

    #zip_ref.extractall(distDir)

    #zip_ref.close()



    #zipApk(workingdir)

    # Remove old signature
    #shutil.rmtree(os.path.join(workingdir, "META-INF"))


def getApkDestinationFolder(apk):
    apkPath = Path(apk)
    print(f"apk path {apkPath}")

    appFolder = apkPath.stem

    script = os.path.dirname(__file__)
    homeDir = Path(script).parent.absolute()
    workDir = Path(homeDir / "workDir")
    destDir = Path(workDir / appFolder)

    return destDir
def getApkAnylDestinationFolder(apk):
    apkPath = Path(apk)
    print(f"apk path {apkPath}")

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
    print(f"to be aligned Apk: {srcApkPath}")

    zipAlignCommand = 'zipalign -p -f -v 4 '
    argApk = f'{srcApkPath} {alignedApkPath}'

    for i in range(4):
        print(f'i = {i}')
        if exists(srcApkPath) and i == 3:
            process = os.system( zipAlignCommand + argApk )
            break
        time.sleep(1)









#generateCert(outKeyFile,cName,orgUnit,org,location,state,country,newKeyPass,newStorePass,newAlias)

#print(" Signing the APK")

#unzipApk(apk)
#signApk(apk,outKeyFile,newStorePass,newKeyPass,newAlias)

