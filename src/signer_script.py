
import zipfile
import shutil
import subprocess
import tempfile
import os
import pathlib
from pathlib import Path



def testSignApk(apk):
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
        print(p.stdout.decode("utf8"))

def signApk(apk,keyPath,storePass,keyPass,alias):

    if 1>0:
        print("apk signer")
        print(os.getcwd())
        apk_sign_comm = f"C:\\Users\\Afif\\python_projects\\afif_android_tool\\src\\apksigner.bat sign --v2-signing-enabled --ks {keyPath} --ks-key-alias {alias} --ks-pass pass:{storePass} --key-pass pass:{keyPass} {apk}"

        p = subprocess.run(apk_sign_comm, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, check=False)
        if p.returncode > 0:
            print(p.stdout.decode("utf8"))


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




# create cert
def generateCert(outKeyFile,CName,orgUint,org,loc,state,country,keyPass,storePass,alias):
    print(f"out from signer {CName}")


    keytool = f'keytool -genkey -v -keystore {outKeyFile} -dname "CN={CName}, OU={orgUint}, O={org}, L={loc}, S={state}, C={country}" -keypass {keyPass} -storepass {storePass} -alias {alias} -keyalg RSA -keysize 2048 -validity 10000'
    os.system(keytool)


ADB = shutil.which("adb")

def unzipApk(apk):

    workingdir = tempfile.mkdtemp(suffix='apkWorkingDir')
    # Unzip
    print(" Unzip the apk file in workingdir ")
    zip_ref = zipfile.ZipFile(apk, 'r')
    cwd = os.getcwd()
    apkPath = Path(apk)
    appFolder = apkPath.stem
    # appFolder = f'{cwd}\{apk.name}'

    print(f"app folder{appFolder}  ")
    script = os.path.dirname(__file__)
    homeDir = Path(script).parent.absolute()
    workDir = Path(homeDir/"workDir")
    distDir = Path(workDir/appFolder)


    zip_ref.extractall(distDir)

    print(f"dist folder path {script}")
    # zip_ref.close()



    return distDir

    #zipApk(workingdir)

    # Remove old signature
    #shutil.rmtree(os.path.join(workingdir, "META-INF"))

def zipApk(appFolder):

    # Zip
    print("start APK Building")
    shutil.make_archive("new", 'zip', appFolder)
    shutil.move("new.zip", "nat_zipped.apk")




#generateCert(outKeyFile,cName,orgUnit,org,location,state,country,newKeyPass,newStorePass,newAlias)

#print(" Signing the APK")

#unzipApk(apk)
#signApk(apk,outKeyFile,newStorePass,newKeyPass,newAlias)

