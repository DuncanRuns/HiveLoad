from threading import Thread
from world_upload import upload
from win32 import win32gui
import pygame
import json
import os
import time
import traceback
import shutil
import tkinter as tk

minecraftPath = ""
running = False
highSound: pygame.mixer.Sound = None
lowSound: pygame.mixer.Sound = None
uploadingSound: pygame.mixer.Sound = None


def resource_path(relative_path):
    try:
        from sys import _MEIPASS
        base_path = _MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def isSinglePlayerOpen() -> bool:
    window = win32gui.GetForegroundWindow()
    text = win32gui.GetWindowText(window)
    return " - Singleplayer" in text and "Minecraft" in text


def runMacro(*x):
    global running, minecraftPath, highSound, lowSound, uploadingSound
    if not running:
        if not isSinglePlayerOpen():
            Thread(target=uploadingSound.play).start()
            running = True
            try:
                savesPath = os.path.join(minecraftPath, "saves")

                with open(os.path.join(minecraftPath, "attempts.txt"), "r") as attemptsFile:
                    attempts = attemptsFile.read().rstrip()
                    attemptsFile.close()

                worldName = "Speedrun #"+attempts
                
                shutil.make_archive(worldName,"zip",os.path.join(savesPath,worldName))

                upload(worldName+".zip","")
                
                os.remove(worldName+".zip")

                with open("done", "w") as doneFile:
                    doneFile.write("omg how did you find this epic secret omg")
                    doneFile.close()

                upload("done", "")
                os.remove("done")

            except:
                print("Failed")
                traceback.print_exc()
            running = False
            Thread(target=highSound.play).start()
        else:
            Thread(target=lowSound.play).start()


if __name__ == "__main__":
    with open("hiveload.json", "r") as jsonFile:
        jsonDict = json.load(jsonFile)
        jsonFile.close()
    minecraftPath = jsonDict["path"]

    pygame.init()
    pygame.mixer.init()

    highSound = pygame.mixer.Sound(resource_path("high.mp3"))
    lowSound = pygame.mixer.Sound(resource_path("low.mp3"))
    uploadingSound = pygame.mixer.Sound(resource_path("uploading.mp3"))

    highSound.set_volume(0.1)
    lowSound.set_volume(0.1)
    uploadingSound.set_volume(0.1)
    
    
    root = tk.Tk()
    root.title("Hiveload Client")
    root.resizable(0,0)
    root.wm_attributes("-topmost",True)
    tk.Label(root,text="Hiveload Client™\nPress the button to upload your latest world.\nMake sure you are not in the world when uploading.",anchor=tk.CENTER).grid(row=0,column=0,padx=10,pady=5)
    tk.Button(root,command=runMacro,text="Upload World").grid(row=1,column=0,padx=0,pady=5)
    root.mainloop()