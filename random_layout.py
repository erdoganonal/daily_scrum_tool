"Creates a layout that shows next person"
import sys
import os.path
import re

from string import printable
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from layout_base import SingleLayoutBase, States
from names import Names
from constants import PAD, DEFAULT_PHOTO, IMAGE_SIZE, THE_END_PHOTO, IMAGE_ALLOWED_TYPES
import texts

class RandomNameDisplayerLayout(SingleLayoutBase):
    "Creates a layout that shows next person"

    def __init__(self, root, context, **grid_options):
        super().__init__(root, context, **grid_options)
        self._winner = None
        self._names = None

        image_frame = tk.Frame(self.parent)
        image_frame.grid(sticky=tk.NSEW, pady=(0, PAD))

        self._winner_name_label = tk.Label(image_frame, width=2*PAD)
        self._winner_name_label.grid()

        self._winner_photo_label = tk.Label(image_frame)
        self._winner_photo_label.grid(sticky=tk.NSEW)

    @staticmethod
    def _set_photo(label, image):
        resized = image.resize(IMAGE_SIZE, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized)

        label.configure(image=photo)

        # Below variable assigment is required to force a
        # strong reference on the instance.
        label.image = photo

    def valid_image_extension(self, image_name):
        image_name = re.sub("[^{}]+".format(printable), "", image_name)
        pattern = re.compile(r"(" + image_name +
                             "(\\.(?i)("+IMAGE_ALLOWED_TYPES+"))$)", re.IGNORECASE)

        for filepath in os.listdir(self.config.paths.photos):
            if pattern.match(filepath):
                image_name = filepath
        return image_name

    def _configure_label_image(self, label, image_name):
        try:
            if image_name:
                image_name = self.valid_image_extension(image_name)
            image_path = "{0}/{1}".format(
                self.config.paths.photos, image_name
            )
            image = Image.open(image_path)
        except (FileNotFoundError, OSError, KeyError):
            try:
                image = Image.open(DEFAULT_PHOTO)
            except (FileNotFoundError, OSError):
                messagebox.showerror(
                    texts.RANDOM_FILE_NOT_EXIST_TITLE,
                    texts.RANDOM_FILE_NOT_EXIST_MSG.format(DEFAULT_PHOTO)
                )
                sys.exit()

        self._set_photo(label, image)

    def _clean(self):
        self._winner_name_label.configure(text="")
        self._configure_label_image(
            self._winner_photo_label, DEFAULT_PHOTO
        )

    def handle_init(self):
        self._clean()

    def handle_startup(self):
        "On startup, load names and get the next person"
        if self._names is None:
            try:
                self._names = Names(self.config.paths.names)
            except FileNotFoundError:
                self._context.state = States.INITIAL
                messagebox.showerror(
                    texts.RANDOM_FILE_NOT_EXIST_TITLE,
                    texts.RANDOM_FILE_NOT_EXIST_MSG.format(
                        self.config.paths.names)
                )
                return
        else:
            self._names.reload(self.config.paths.names)

        # pass names to context to use it in random layout
        self._context.set_item("names", self._names)

        self._clean()
        self.get_next_person()

    def handle_next(self):
        "On next, display next person"
        self.get_next_person()

    def handle_timeout(self):
        "Do nothing"

    def handle_reset(self):
        "On reset, need to start over. Clean the screen and display a message"
        self._clean()
        image = Image.open(THE_END_PHOTO)
        self._set_photo(self._winner_photo_label, image)

        self._winner_name_label.configure(
            text=texts.RANDOM_REACH_END
        )

    def get_next_person(self):
        "Display next person"
        try:
            winner = self._names.pick_and_remove().strip()
        except IndexError:
            self._context.state = States.RESET
            return

        self._winner_name_label.configure(text=winner)
        self._configure_label_image(self._winner_photo_label, winner)
