from ftplib import FTP
import json
import os

def uploadFolder(ftp: FTP, path: str, localwd: str, serverwd: str):
    print("Creating folder "+path+"...")
    ftp.mkd(os.path.join(serverwd,path).replace("\\","/"))
    for name in os.listdir(os.path.join(localwd, path)):
        localpath = os.path.join(localwd, path, name)
        if os.path.isfile(localpath):
            uploadFile(ftp, os.path.join(path, name), localwd, serverwd)
        elif os.path.isdir(localpath):
            uploadFolder(ftp, os.path.join(path, name), localwd, serverwd)


def uploadFile(ftp: FTP, path: str, localwd: str, serverwd: str):
    print("Uploading "+path+"...")
    ftp.storbinary("STOR "+os.path.join(serverwd,path).replace("\\","/"),open(os.path.join(localwd,path),"rb"))


def upload(path: str, localwd: str):
    with open("ftp.json", "r") as jsonFile:
        jsonDict = json.load(jsonFile)
        jsonFile.close()

    serverwd = jsonDict["location"]

    ftp = FTP(host=jsonDict["host"],
              user=jsonDict["user"], passwd=jsonDict["password"])
    if os.path.isdir(os.path.join(localwd,path)):
        uploadFolder(ftp, path, localwd, serverwd)
    elif os.path.isfile(os.path.join(localwd,path)):
        uploadFile(ftp, path, localwd, serverwd)


if __name__ == "__main__":
    upload("test", "saves")