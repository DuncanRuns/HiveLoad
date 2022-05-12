import os, time, shutil, json, traceback
import python_nbt.nbt as nbt

enableWL = True


def enable_whitelist() -> None:
    print("Re-enabling whitelist")
    with open("server.properties", "r") as prop_file:
        text = prop_file.read()
        prop_file.close()
    with open("server.properties", "w+") as prop_file:
        prop_file.write(text.replace(
            "white-list=false", "white-list=true"))
        prop_file.close()


def clear_input_folder(input_path: str) -> None:
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


# Check version from level.dat, setup
def setup_jars():
    [shutil.rmtree(i) for i in ["mods",
                                "libraries"] if os.path.isdir(i)]
    [os.remove(i) for i in ["fabric-server-launch.jar",
                            "server.jar"] if os.path.isfile(i)]
    try:
        mc_version = nbt.read_from_nbt_file(
            "world/level.dat")["Data"]["Version"]["Name"].value
        shutil.copytree(os.path.join(
            os.getcwd(), "versions", mc_version), os.getcwd(), dirs_exist_ok=True)
    except:
        traceback.print_exc()
        print("Failed to get server files for minecraft version.")


def copy_and_run(done_path: str, input_path: str, command: str) -> None:
    print("Copying world and running...")
    os.remove(done_path)
    try:
        world_path = os.path.join(input_path, os.listdir(input_path)[0])
        if world_path.endswith(".zip"):
            world_path = world_path[:-4]
            os.mkdir(world_path)
            shutil.unpack_archive(world_path + ".zip", world_path)
        shutil.copytree(world_path, "world")
        for name in os.listdir(input_path):
            rm_path = os.path.join(input_path, name)
            if(os.path.isfile(rm_path)):
                os.remove(rm_path)
            else:
                shutil.rmtree(rm_path)
        setup_jars()
        os.system(command)
    except:
        traceback.print_exc()


def main():

    with open("hiveload.json", "r") as jsonFile:
        jsonDict = json.load(jsonFile)
        jsonFile.close()

    input_path = jsonDict["input"]
    command = jsonDict["command"]
    done_path = os.path.join(input_path, "done")

    while True:
        if os.path.isdir("world"):
            delete_world()
        if enableWL:
            enable_whitelist()
        clear_input_folder(input_path)
        print("CHECKING")
        while not os.path.isfile(os.path.join(input_path, "done")):
            time.sleep(1)
        copy_and_run(done_path, input_path, command)


if __name__ == "__main__":
    main()
