import os
import time
import shutil
import json, traceback

enableWL = True

if __name__ == "__main__":

    with open("hiveload.json","r") as jsonFile:
        jsonDict = json.load(jsonFile)
        jsonFile.close()

    inputPath = jsonDict["input"]
    command = jsonDict["command"]
    donePath = os.path.join(inputPath,"done")

    while True:
        if os.path.isdir("world"):
            print("Removing world...")
            shutil.rmtree("world")
        if enableWL:
            print("Re enabling whitelist")
            with open("server.properties","r") as propFile:
                text = propFile.read()
                propFile.close()
            with open("server.properties","w+") as propFile:
                propFile.write(text.replace("white-list=false","white-list=true"))
                propFile.close()
        print("CHECKING")
        while not os.path.isfile(os.path.join(inputPath,"done")):
            time.sleep(1)
        print("Copying world and running...")
        os.remove(donePath)
        try:
            worldPath = os.path.join(inputPath,os.listdir(inputPath)[0])
            shutil.copytree(worldPath,"world")
            for name in os.listdir(inputPath):
                shutil.rmtree(os.path.join(inputPath,name))
            os.system(command)
        except:
            traceback.print_exc()