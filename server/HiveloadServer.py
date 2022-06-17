import os, time, shutil, json, traceback, random
from typing import Union
import python_nbt.nbt as nbt

ENABLE_WL = True


def set_random_icon() -> None:
    print("Setting random icon...")
    if os.path.isfile("server-icon.png"):
        os.remove("server-icon.png")
    icons = [i for i in os.listdir("icons")]
    if icons:
        choice = random.choice(icons)
        shutil.copyfile(os.path.join("icons", choice), "server-icon.png")


def enable_whitelist() -> None:
    print("Re-enabling whitelist...")
    with open("server.properties", "r") as prop_file:
        text = prop_file.read()
        prop_file.close()
    with open("server.properties", "w+") as prop_file:
        prop_file.write(text.replace(
            "white-list=false", "white-list=true"))
        prop_file.close()


def clear_input_folder(input_path: str) -> None:
    """No longer in use"""
    print("Removing extra worlds...")
    for name in os.listdir(input_path):
        rm_path = os.path.join(input_path, name)
        if(os.path.isfile(rm_path)):
            os.remove(rm_path)
        else:
            shutil.rmtree(rm_path)


def delete_world() -> None:
    print("Removing world...")
    shutil.rmtree("world")


# Clear version related files, check version from level.dat, copy from versions folder
def setup_jars():
    [shutil.rmtree(i) for i in ["mods",
                                "libraries"] if os.path.isdir(i)]
    [os.remove(i) for i in ["fabric-server-launch.jar",
                            "server.jar"] if os.path.isfile(i)]
    try:
        mc_version = nbt.read_from_nbt_file(
            "world/level.dat")["Data"]["Version"]["Name"].value
        print("World version is", mc_version)
        shutil.copytree(os.path.join(
            os.getcwd(), "sversions", mc_version), os.getcwd(), dirs_exist_ok=True)
    except:
        traceback.print_exc()
        print("Failed to get server files for minecraft version.")


def copy_and_run(input_path: str, command: str) -> None:
    print("Copying world and running...")
    try:
        world_path = get_any_world(input_path)
        if world_path.endswith(".zip"):
            world_path = world_path[:-4]
            os.mkdir(world_path)
            shutil.unpack_archive(world_path + ".zip", world_path)
            os.remove(world_path + ".zip")
        shutil.copytree(world_path, "world")
        if os.path.isfile(world_path):
            os.remove(world_path)
        else:
            shutil.rmtree(world_path)
        setup_jars()
        os.system(command)
    except:
        traceback.print_exc()


def wait_for_done_file(done_path: str) -> None:
    print("Waiting for done file...")
    while not os.path.isfile(done_path):
        time.sleep(1)
    os.remove(done_path)


def get_any_world(input_path: str) -> Union[None, str]:
    for name in os.listdir(input_path):
        if name != "done" and not name.lower().endswith(".hld"):
            return os.path.join(input_path, name)


def main():

    with open("hiveload.json", "r") as jsonFile:
        jsonDict = json.load(jsonFile)
        jsonFile.close()

    input_path = jsonDict["input"]
    command = jsonDict["command"]
    done_path = os.path.join(input_path, "done")

    while True:
        time.sleep(1)
        if os.path.isdir("icons"):
            set_random_icon()
        if os.path.isdir("world"):
            delete_world()
        if ENABLE_WL:
            enable_whitelist()
        if get_any_world(input_path) is None:
            wait_for_done_file(done_path)
        copy_and_run(input_path, command)


if __name__ == "__main__":
    main()
