import os, time, shutil, traceback, random, basic_options, subprocess
from typing import Union
import python_nbt.nbt as nbt


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


def copy_and_run(input_path: str, command: str, world_location: str) -> None:
    if os.path.isfile("done"):
        os.remove("done")
    print("Copying world and running...")
    try:
        world_path = get_first_world(input_path)
        if world_path.endswith(".zip"):
            world_path = world_path[:-4]
            os.mkdir(world_path)
            shutil.unpack_archive(world_path + ".zip", world_path)
            os.remove(world_path + ".zip")
        shutil.copytree(world_path, world_location)
        if os.path.isfile(world_path):
            os.remove(world_path)
        else:
            shutil.rmtree(world_path)
        setup_jars()
        os.system(command)
    except:
        traceback.print_exc()


def wait_for_done_file(done_path: str, waiting_command: str, waiting_dir: str) -> None:
    process_opened = False
    if waiting_command != "" and not os.path.isfile(done_path):
        print("Starting waiting command...")
        process_opened = True
        process = subprocess.Popen(
            waiting_command, stdin=subprocess.PIPE, cwd=waiting_dir, shell=True)

    print("Waiting for done file...")
    while not os.path.isfile(done_path):
        time.sleep(1)

    if process_opened:
        print("Attempting to stop server...")
        process.stdin.write("stop".encode())
        process.stdin.flush()
        print("Stop command sent...")
        process.communicate()

    os.remove(done_path)


def get_first_world(input_path: str) -> Union[None, str]:
    files = [os.path.join(input_path, name)
             for name in os.listdir(input_path) if name != "done"]
    files.sort(key=lambda x: os.path.getmtime(x))
    for file_path in files:
        if not file_path.lower().endswith(".hld"):
            return file_path


class Options(basic_options.BasicOptions):
    def set_defaults(self) -> None:
        self.input = "input"
        self.auto_whitelist = True

        self.world_location = "world"
        self.command = "java -jar fabric-server-launch.jar nogui"

        self.waiting_command = ""
        self.waiting_dir = "waiting"


def main():

    options = Options().try_load_file("hiveload.json")
    options.save_file("hiveload.json")

    done_path = os.path.join(options["input"], "done")

    while True:
        time.sleep(1)

        if os.path.isdir("icons"):
            set_random_icon()

        if os.path.isdir("world"):
            delete_world()

        if options["auto_whitelist"]:
            enable_whitelist()

        if get_first_world(options["input"]) is None:
            wait_for_done_file(
                done_path, options["waiting_command"], options["waiting_dir"])

        if get_first_world(options["input"]):
            copy_and_run(options["input"], options["command"],
                         options["world_location"])


if __name__ == "__main__":
    main()
