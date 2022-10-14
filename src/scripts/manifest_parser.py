import pathlib
import re
from scripts.model.Activity import Activity
from scripts.model.Receiver import Receiver

#project = "src\deb_tool"



def openManifest(self,project):
    for path in pathlib.Path(project).iterdir():
        manifestName = "AndroidManifest.xml"
        print(f'file name before open{ path.name}')
        if path.name == manifestName:
            return path




def getPackageName(self,manifest):
  packageName = ""
  package = "package="
  with open(manifest, 'r') as f:
      for line in f:

          if line.__contains__(package):
              apkInfoLine = line.split(' ')
              for item in apkInfoLine:
                  if item.__contains__("package"):

                      packageName = item[9:len(item) - 1]
                      print(f"packageName : {packageName}")



  return packageName


def getActivities(self,manifest):
    arrActivities = []
    activityTag = "<activity"
    endActivityTag = "</activity>"
    actionMain = "action.MAIN"
    androidName = "android:name"
    androidExported = 'android:exported="true"'
    with open(manifest, 'r') as f:
        activityName = ""
        actNameFound = False
        inActivityTag = False
        lanuchAbleAct = False
        for line in f:
            if line.__contains__(activityTag):

                inActivityTag = True
                actNameFound = False
                splittedLine = re.split(r'( |>)', line)

                for attribute in splittedLine:

                    if attribute.__contains__(androidName):
                        activityFullName = attribute.split('.')
                        actNameFound = True
                        activityName = activityFullName[-1][0:-1]

                    if attribute.__contains__(androidExported):
                        lanuchAbleAct = True

            if not actNameFound and inActivityTag:
                if line.__contains__(androidName):
                    splittedLine = re.split(r'( |>)', line)

                    for attribute in splittedLine:

                        if attribute.__contains__(androidName):
                            activityFullName = attribute.split('.')

                            actNameFound = True
                            activityName = activityFullName[-1][0:-1]

                        if attribute.__contains__(androidExported):
                            lanuchAbleAct = True

            if line.__contains__(androidExported) and inActivityTag:
                lanuchAbleAct = True

            if line.__contains__(actionMain) and inActivityTag:
                print(f'{activityName} has main')
                lanuchAbleAct = True

            if line.__contains__(endActivityTag):
                inActivityTag = False
                if lanuchAbleAct:
                    print(f'launchable')

                    activity = Activity(activityName, True)
                    arrActivities.append(activity)
                    lanuchAbleAct = False

                else:
                    print(f'not launchable')


    return arrActivities

def getReceivers(self,manifest):
    arrReceivers = []
    receiverTag = "<receiver"
    endReceiverTag = "</receiver>"
    androidName = "android:name"
    androidExported = 'android:exported="true"'
    actionTag = "<action"

    with open(manifest, 'r') as f:
        receiverName = ""
        action = ""
        recNameFound = False
        inReceiverTag = False
        lanuchAbleRec = False
        for line in f:
            if line.__contains__(receiverTag):

                inReceiverTag = True
                recNameFound = False
                splittedLine = re.split(r'( |>)', line)

                for attribute in splittedLine:

                    if attribute.__contains__(androidName):
                        print(f"attribute  : {attribute}")
                        receiverFullName = attribute.split('.')

                        recNameFound = True
                        receiverName = receiverFullName[-1][0:-1]

                    if attribute.__contains__(androidExported):
                        lanuchAbleRec = True

            if not recNameFound and inReceiverTag:
                if line.__contains__(androidName):
                    splittedLine = re.split(r'( |>)', line)

                    for attribute in splittedLine:

                        if attribute.__contains__(androidName):
                            print(f"attribute  : {attribute}")
                            receiverFullName = attribute.split('.')

                            recNameFound = True
                            receiverName = receiverFullName[-1][0:-1]

                        if attribute.__contains__(androidExported):
                            lanuchAbleRec = True

            if line.__contains__(androidExported) and inReceiverTag:
                lanuchAbleRec = True

            if line.__contains__(actionTag) and inReceiverTag:

                print(f'{receiverName} has action')
                lanuchAbleRec = True
                splittedLine = re.split(r'( |/>)', line)

                for attribute in splittedLine:

                    if attribute.__contains__(androidName):
                        print(f"attribute  : {attribute}")
                        actionFullName = attribute.split('"')

                        action = actionFullName[-2]
                        print(f"actionName  : {action}")

            if line.__contains__(endReceiverTag):
                inReceiverTag = False
                if lanuchAbleRec:
                    print(f'launchable')

                    receiver = Receiver(receiverName, action, True)
                    arrReceivers.append(receiver)
                    lanuchAbleRec = False

                else:
                    print(f'not launchable')


    return arrReceivers



#def getPackageName(self)