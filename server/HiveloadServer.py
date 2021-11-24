import os
import time
import shutil
import json
import traceback

enableWL = True

if __name__ == "__main__":

    with open("hiveload.json", "r") as jsonFile:
        jsonDict = json.load(jsonFile)
        jsonFile.close()

    inputPath = jsonDict["input"]
    command = jsonDict["command"]
    donePath = os.path.join(inputPath, "done")

    while True:

        if os.path.isdir("world"):
            print("Removing world...")
            shutil.rmtree("world")

        if enableWL:
            print("Re enabling whitelist")
            with open("server.properties", "r") as propFile:
                text = propFile.read()
                propFile.close()
            with open("server.properties", "w+") as propFile:
                propFile.write(text.replace(
                    "white-list=false", "white-list=true"))
                propFile.close()

        print("Removing extra worlds...")
        for name in os.listdir(inputPath):
            rmPath = os.path.join(inputPath, name)
            if(os.path.isfile(rmPath)):
                os.remove(rmPath)
            else:
                shutil.rmtree(rmPath)

        print("CHECKING")
        while not os.path.isfile(os.path.join(inputPath, "done")):
            time.sleep(1)

        print("Copying world and running...")
        os.remove(donePath)
        try:
            worldPath = os.path.join(inputPath, os.listdir(inputPath)[0])
            if worldPath.endswith(".zip"):
                worldPath = worldPath[:-4]
                os.mkdir(worldPath)
                shutil.unpack_archive(worldPath+".zip", worldPath)
            shutil.copytree(worldPath, "world")
            for name in os.listdir(inputPath):
                rmPath = os.path.join(inputPath, name)
                if(os.path.isfile(rmPath)):
                    os.remove(rmPath)
                else:
                    shutil.rmtree(rmPath)

            os.system(command)
        except:
            traceback.print_exc()
