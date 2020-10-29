"""Constants for the program"""
import sys
import os

BASE_PATH = os.path.abspath(
    getattr(sys, "_MEIPASS", os.path.dirname(sys.argv[0]))
)

SOURCE_FOLDER = os.path.join(BASE_PATH, "sources")
DEFAULT_PHOTO = os.path.join(SOURCE_FOLDER, "default.png")
CLOCK_IMAGE_PATH = os.path.join(SOURCE_FOLDER, "clock.png")
THE_END_PHOTO = os.path.join(SOURCE_FOLDER, "theend.png")
IMAGE_SIZE = (200, 200)

PAD = 15
LAYOUT_BG = "#C3EAE9"

# Button
BUTTON_BG = "#13ACAC"
BUTTON_FG = "#2A0527"
BUTTON_FONT = ('Comic Sans MS', 11, 'bold')

# Config
DEFAULT_CONFIG = os.path.join(SOURCE_FOLDER, "config.json")
CFG_ALLOWED_TYPES = (("JSON File", "*.json"),)
IMAGE_ALLOWED_TYPES ="jpg|jpeg|png|gif|bmp"

# Label
LABEL_DFT_FG = "#AD1212"
LABEL_DFT_FONT = ('Comic Sans MS', 14, 'bold')

# Menu
MENU_BTN_FONT = (None, 9, "bold")
