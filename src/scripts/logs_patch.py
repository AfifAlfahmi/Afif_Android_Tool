
import os,re
import pathlib



def logFunName(project,packageName):
    for smaliFolder in pathlib.Path(project).iterdir():

        if smaliFolder.is_dir():
            if smaliFolder.name.__contains__("smali"):

                for subPack1 in pathlib.Path(smaliFolder).iterdir():
                    if packageName.__contains__(subPack1.name):
                        #found subPack1 com folder

                        for subPack2 in pathlib.Path(subPack1).iterdir():
                            if packageName.__contains__(subPack2.name):
                                #found  subPack2 folder

                                for subPack3 in pathlib.Path(subPack2).iterdir():

                                    # #
                                    if subPack3.name.__contains__('.smali'):
                                        smaliFileName = smaliFile.name
                                        if not smaliFileName.__contains__('$'):
                                            logClassMethodName(subPack3)

                                    if packageName.__contains__(subPack3.name):
                                        #found subPack3 folder
                                        smaliFileName = ""
                                        for smaliFile in pathlib.Path(subPack3).iterdir():

                                            # check if file or package
                                            if os.path.isfile(smaliFile) :

                                                smaliFileName = smaliFile.name
                                                if not smaliFileName.__contains__('$'):
                                                    logClassMethodName(smaliFile)

                                            #internal packages
                                            else:

                                                for smaliFile2 in pathlib.Path(smaliFile).iterdir():

                                                    smaliFileName = smaliFile2.name
                                                    if not smaliFileName.__contains__('$'):

                                                        logClassMethodName(smaliFile2)

                                    else:

                                        for smaliFile in pathlib.Path(subPack3).iterdir():
                                            if os.path.isfile(smaliFile) :
                                                smaliFileName = smaliFile.name
                                                if not smaliFileName.__contains__('$'):

                                                    logClassMethodName(smaliFile)




def  logClassMethodName(path4):
      smaliFileName = path4.name
      with open(path4) as smaliFile, open(f"{smaliFile.name}out.smali", "w") as smaliOut:
          className = ""
          methodName = ""

          inMethod = False
          currentLine = 0
          prevLine = ""
          retSet = False
          numOfLocal = 0
          numOfParam = 0

          for i, line in enumerate(smaliFile):

              if line.startswith(".class"):
                  splittedLine = re.split(r'( )', line)
                  className = splittedLine[-1][0:-2]

              if line.startswith(".method") :
                  if line.__contains__('constructor'):
                      methodName = "constructor"


                  else:
                      splittedLine = re.split(r'( )', line)
                      fullmethodname = splittedLine[-1]
                      endName = fullmethodname.index("(")
                      inMethod = True
                      methodName = fullmethodname[0:endName]



              if line.__contains__('.param') and inMethod:
                  numOfParam = numOfParam + 1


              if line.__contains__('.locals') and not methodName.__contains__('constructor') and not methodName.__contains__('$'):
                  newLocals = 0
                  splittedLine = re.split(r'( )', line)
                  numOfLocal = int(splittedLine[-1])

                  if numOfLocal == 0 or numOfLocal == 1:

                      newLocals = 2
                  else:
                      newLocals = numOfLocal

                  line = f'    {splittedLine[-3]} {newLocals}\n'\
                   f'\n    const-string v0, "patchTag"\n\n' \
                    f'    const-string v1, "class: {className} method: {methodName}"\n\n' \
                    f'    invoke-static {{v0,v1}}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I\n\n'
                  smaliOut.write(line)
              else:
                  smaliOut.write(line)

              if line.startswith(".end method"):
                  inMethod = False
                  retSet = False
                  numOfParam = 0
                  numOfLocal = 0

              if inMethod and line.__contains__(".line"):
                  splittedLineNum = re.split(r'( )', line)

                  currentLine = splittedLineNum[-1]

              # if line.__contains__("return") and inMethod:
              #
              #     print(f'numOfParam : {numOfParam}')
              #
              #     # if numOfLocal + numOfParam <= 14 :
              #     print(f'in return prev line{prevLine}')
              #     inMethod = False
              #     inMethodContent = False
              #     retSet = True
              #     prevLine = prevLine + f'\n    const-string v{numOfLocal}, "funTag"\n\n' \
              #                           f'    const-string v{numOfLocal + 1}, "class: {className} method: {methodName}"\n\n' \
              #                           f'    invoke-static {{v{numOfLocal},v{numOfLocal + 1}}}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I\n\n'
              #     smaliOut.write(prevLine)
              #
              #     prevLine = f'    .line {int(currentLine) + 1}\n{line}'
              #     smaliOut.write(prevLine)



                      #splittedLine = re.split(r'( )', line)
                      #returnReg = int(splittedLine[-1])

              # else:
              #     if line.__contains__('.end method'):
              #
              #         smaliOut.write(line)
              #         print(f'in .end method line{line}')
              #         inMethod = False
              #
              #
              #     else:
              #         if inMethod:
              #             if line.__contains__('.method'):
              #                 print(f'start of method{line}')
              #                 prevLine = line
              #
              #             else:
              #                 smaliOut.write(prevLine)
              #                 print(f'else in  method{line}')
              #                 prevLine = line
              #
              #
              #         else:
              #             smaliOut.write(line)
              #
              #             print(f'else not in  method{line}')

          smaliFile.close()

          smaliOut.close()

          os.remove(smaliFile.name)
          # Rename dummy file as the original file
          path = pathlib.Path(smaliFile.name).parent.resolve()
          # path for the new
          os.rename(smaliOut.name, f'{path}/{smaliFileName}')


















