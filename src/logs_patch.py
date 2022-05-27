import shutil
import zipfile
import tempfile
import os,re
import pathlib






def logFunName(project,packageName):
    for path in pathlib.Path(project).iterdir():

        if path.is_dir():
            if path.name.__contains__("smali"):
                for path2 in pathlib.Path(path).iterdir():
                    print(f"inside smali folder{path2.name}")
                    if path2.name.__contains__("com"):
                        print(f"inside com folder")
                        for path3 in pathlib.Path(path2).iterdir():
                            if packageName.__contains__(path3.name):
                                print(f"inside path3 folder")

                                for path4 in pathlib.Path(path3).iterdir():

                                    if packageName.__contains__(path4.name):
                                        print(f"inside path4 folder")
                                        smaliFileName = ""
                                        for smaliFile in pathlib.Path(path4).iterdir():
                                            smaliFileName = smaliFile.name
                                            if smaliFile.name == "MainActivity.smali":
                                                with open(smaliFile) as smaliFile,open(f"{smaliFile.name}out.smali","w") as smaliOut:
                                                    className = ""
                                                    methodName = ""

                                                    inMethod = False
                                                    currentLine = 0
                                                    prevLine = ""
                                                    retSet = False
                                                    numOfLocal = 0

                                                    for i,line in enumerate(smaliFile):

                                                        if line.startswith(".class"):

                                                            splittedLine = re.split(r'( )', line)
                                                            className = splittedLine[-1][0:-2]
                                                            print(f"class name: {className}")

                                                        if line.startswith(".method") and not line.__contains__('constructor '):
                                                            splittedLine = re.split(r'( )', line)
                                                            fullmethodname = splittedLine[-1]
                                                            endName = fullmethodname.index("(")
                                                            inMethod = True
                                                            methodName =fullmethodname[0:endName]
                                                            print(f"found method: {methodName} end: {endName}")

                                                        if line.__contains__('.locals'):
                                                            splittedLine = re.split(r'( )', line)
                                                            numOfLocal = int(splittedLine[-1])
                                                            print(f'type of numOfLocal {type(numOfLocal)} value: {numOfLocal}')
                                                            print(f'numOfLocal all {splittedLine}')

                                                            print(f'numOfLocal [-2]{splittedLine[-2]}')
                                                            print(f'numOfLocal [-3]{splittedLine[-3]}')
                                                            line = f'    {splittedLine[-3]} {numOfLocal+2}\n'

                                                        if line.startswith(".end method"):
                                                            inMethod = False
                                                            retSet = False
                                                        if inMethod and line.__contains__(".line"):
                                                            splittedLineNum = re.split(r'( )', line)

                                                            currentLine = splittedLineNum[-1]
                                                            print(f"splitted Line Num: {currentLine}")

                                                        if line.__contains__("return") and inMethod:
                                                            print(f'in return prev line{prevLine}')
                                                            inMethod = False
                                                            inMethodContent = False
                                                            retSet = True
                                                            prevLine = prevLine + f'\n    const-string v{numOfLocal}, "funTag"\n\n' \
                                                                                  f'    const-string v{numOfLocal + 1}, "class: {className} method: {methodName}"\n\n' \
                                                                                  f'    invoke-static {{v{numOfLocal},v{numOfLocal + 1}}}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I\n\n'
                                                            smaliOut.write(prevLine)

                                                            prevLine = f'    .line {int(currentLine)+1}\n{line}'
                                                            smaliOut.write(prevLine)


                                                        else:
                                                            if line.__contains__('.end method'):

                                                                smaliOut.write(line)
                                                                print(f'in .end method line{line}')
                                                                inMethod = False


                                                            else:
                                                                if inMethod:
                                                                    if line.__contains__('.method'):
                                                                        print(f'start of method{line}')
                                                                        prevLine = line

                                                                    else:
                                                                        smaliOut.write(prevLine)
                                                                        print(f'else in  method{line}')
                                                                        prevLine = line


                                                                else:
                                                                    smaliOut.write(line)

                                                                    print(f'else not in  method{line}')

                                                    smaliFile.close()
                                                    #smaliOut.write("A fif")

                                                    smaliOut.close()

                                                    os.remove(smaliFile.name)
                                                    # Rename dummy file as the original file
                                                    path = pathlib.Path(smaliFile.name).parent.resolve()
                                                    print(f"path for the new{path}")
                                                    os.rename(smaliOut.name,f'{path}/{smaliFileName}')





def logJavaFunName(project,packageName):
    for path in pathlib.Path(project).iterdir():

        if path.is_dir():
            if path.name.__contains__("smali"):
                for path2 in pathlib.Path(path).iterdir():
                    print(f"inside smali folder{path2.name}")
                    if path2.name.__contains__("com"):
                        print(f"inside com folder")
                        for path3 in pathlib.Path(path2).iterdir():
                            if packageName.__contains__(path3.name):
                                print(f"inside path3 folder")

                                for path4 in pathlib.Path(path3).iterdir():

                                    if packageName.__contains__(path4.name):
                                        print(f"inside path4 folder")
                                        smaliFileName = ""
                                        for smaliFile in pathlib.Path(path4).iterdir():
                                            smaliFileName = smaliFile.name
                                            if smaliFile.name == "JavaActivity.smali":
                                                with open(smaliFile) as smaliFile,open(f"{smaliFile.name}out.smali","w") as smaliOut:
                                                    className = ""
                                                    methodName = ""

                                                    inMethod = False
                                                    currentLine = 0
                                                    prevLine = ""
                                                    retSet = False
                                                    numOfLocal = 0

                                                    for i,line in enumerate(smaliFile):

                                                        if line.startswith(".class"):

                                                            splittedLine = re.split(r'( )', line)
                                                            className = splittedLine[-1][0:-2]
                                                            print(f"class name: {className}")

                                                        if line.startswith(".method") and not line.__contains__('constructor '):
                                                            splittedLine = re.split(r'( )', line)
                                                            fullmethodname = splittedLine[-1]
                                                            endName = fullmethodname.index("(")
                                                            inMethod = True
                                                            methodName =fullmethodname[0:endName]
                                                            print(f" found method: {methodName} end: {endName}")

                                                        if line.__contains__('.locals'):
                                                            splittedLine = re.split(r'( )', line)
                                                            numOfLocal = int(splittedLine[-1])
                                                            print(f'type of numOfLocal {type(numOfLocal)} value: {numOfLocal}')
                                                            print(f'numOfLocal all {splittedLine}')

                                                            print(f'numOfLocal [-2]{splittedLine[-2]}')
                                                            print(f'numOfLocal [-3]{splittedLine[-3]}')
                                                            line = f'    {splittedLine[-3]} {numOfLocal+2}\n'

                                                        if line.startswith(".end method"):
                                                            inMethod = False
                                                            retSet = False
                                                        if inMethod and line.__contains__(".line"):
                                                            splittedLineNum = re.split(r'( )', line)

                                                            currentLine = splittedLineNum[-1]
                                                            print(f"splitted Line Num: {currentLine}")

                                                        if line.__contains__("return") and inMethod:
                                                            print(f'in return prev line{prevLine}')
                                                            inMethod = False
                                                            inMethodContent = False
                                                            retSet = True
                                                            prevLine = prevLine +f'\n    const-string v{numOfLocal}, "funTag"\n\n' \
                                                                        f'    const-string v{numOfLocal+1}, "class: {className} method: {methodName}"\n\n' \
                                                                        f'    invoke-static {{v{numOfLocal},v{numOfLocal+1}}}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I\n\n'
                                                            smaliOut.write(prevLine)

                                                            prevLine = f'    .line {int(currentLine)+1}\n{line}'
                                                            smaliOut.write(prevLine)


                                                        else:
                                                            if line.__contains__('.end method'):

                                                                smaliOut.write(line)
                                                                print(f'in .end method line{line}')
                                                                inMethod = False


                                                            else:
                                                                if inMethod:
                                                                    if line.__contains__('.method'):
                                                                        print(f'start of method{line}')
                                                                        prevLine = line

                                                                    else:
                                                                        smaliOut.write(prevLine)
                                                                        print(f'else in  method{line}')
                                                                        prevLine = line


                                                                else:
                                                                    smaliOut.write(line)

                                                                    print(f'else not in  method{line}')

                                                    smaliFile.close()
                                                    #smaliOut.write("A fif")

                                                    smaliOut.close()

                                                    os.remove(smaliFile.name)
                                                    # Rename dummy file as the original file
                                                    path = pathlib.Path(smaliFile.name).parent.resolve()
                                                    print(f"path for the new{path}")
                                                    os.rename(smaliOut.name,f'{path}/{smaliFileName}')












