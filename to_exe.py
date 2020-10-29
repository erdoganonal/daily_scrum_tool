"""
A script that helps you to create an executable
via Pyinstaller. You should have a clean environment
before building.
"""

import sys
import os
import shutil
import json


SCRIPT_NAME = "daily_scrum_tool"
TEMP_FOLDER_NAME = "build"
SOURCE_FILES = "sources"
MAIN_PATH = os.getcwd()
OUTPUT_FOLDER = "release"
CONFIG_FILE = os.path.join(SOURCE_FILES, "config.json")
DEFAULT_PHOTO = os.path.join(SOURCE_FILES, "default.png")


def main():
    "Starts from here"
    create_temp_env()

    build()

    cleanup()

    exract()


def create_temp_env():
    """Copies entire python files except this file
    into temporary folder"""
    print("Creating a temporary folder")
    if os.path.isdir(TEMP_FOLDER_NAME):
        shutil.rmtree(TEMP_FOLDER_NAME)
    os.makedirs(TEMP_FOLDER_NAME)

    print("Copying the source files")
    for filename in os.listdir("."):
        if filename.endswith(".py"):
            shutil.copy(
                filename,
                os.path.join(TEMP_FOLDER_NAME, filename)
            )

    # Remove this file
    os.unlink(os.path.join(TEMP_FOLDER_NAME, __file__))

    # Now, go to temporary folder
    os.chdir(TEMP_FOLDER_NAME)


def build():
    "Generates an executable via Pyinstaller"
    print("\nBuilding, please wait...")
    ret_val = os.system(
        "pyinstaller.exe "
        "--clean --noconsole  "
        "--onefile "
        "--log-level ERROR "
        "--add-data \"..\\{0};{0}\" "
        "\"{1}.py\""
        "".format(SOURCE_FILES, SCRIPT_NAME)
    )

    os.chdir(MAIN_PATH)
    if ret_val == 0:
        print("Build success")
        # Go back the main folder
        print("Copy the executable")
        exe_name = "{0}.exe".format(SCRIPT_NAME)
        exe_location = os.path.join(TEMP_FOLDER_NAME, "dist", exe_name)

        if os.path.isfile(exe_name):
            os.unlink(exe_name)
        shutil.copy(exe_location, exe_name)
    else:
        cleanup()
        sys.exit("Build failed")


def cleanup():
    "Cleans the temporary files/folders"
    print("\nCleaning up")
    if os.path.isdir(TEMP_FOLDER_NAME):
        shutil.rmtree(TEMP_FOLDER_NAME)


def _copy(source, destination, delete=False):
    basename = os.path.basename(source)
    destination = os.path.join(destination, basename)

    shutil.copy(source, destination)

    if delete:
        os.unlink(source)


def exract():
    "Creating the release"

    print("Creating the release")

    os.chdir(MAIN_PATH)
    if os.path.isdir(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)

    os.makedirs(OUTPUT_FOLDER)

    config = None
    try:
        cfg = open(CONFIG_FILE, 'r')
        config = json.loads(cfg.read())
    except FileNotFoundError:
        sys.exit("Configuration file does not exist")
    except json.JSONDecodeError:
        sys.exit("Configuration file format not valid")
    finally:
        if cfg:
            cfg.close()

    exe_path = SCRIPT_NAME + ".exe"
    names_file = os.path.join(OUTPUT_FOLDER, config["names_file"])
    photos_folder = os.path.join(OUTPUT_FOLDER, config["photos_folder"])

    _copy(exe_path, OUTPUT_FOLDER, delete=True)
    _copy(CONFIG_FILE, OUTPUT_FOLDER)
    with open(names_file, 'w') as names:
        names.write("Your names goes here.\nNewline seperated.")
    os.makedirs(photos_folder)
    _copy(DEFAULT_PHOTO, photos_folder)

    print("Ready to go :)")


if __name__ == "__main__":
    main()
