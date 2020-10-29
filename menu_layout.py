"Creates a layout that allows basic import operation"

import json

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from constants import DEFAULT_CONFIG, CFG_ALLOWED_TYPES
import texts
from layout_base import SingleLayoutBase, States
from config_interface import json_to_config


class ConfigImportError(ImportError):
    "raises when configuration import failed."

    def __init__(self, title, message):
        super().__init__()
        messagebox.showerror(
            title, message
        )


class MenuLayout(SingleLayoutBase):
    "Creates a layout that shows next person"

    def __init__(self, root, context, **grid_options):
        grid_options["sticky"] = tk.W
        super().__init__(root, context, **grid_options)
        self.__is_config_loaded = False

        self._render_file_menu(self.parent)
        self._render_about_menu(self.parent)

    def handle_init(self):
        "On initial, load the configurations"
        if not self.__is_config_loaded:
            self._handle_import(default=True)

    def handle_startup(self):
        "On startup, do nothing"

    def handle_reset(self):
        "On reset, do nothing"

    def handle_next(self):
        "On next, do nothing"

    def handle_timeout(self):
        "On timeout, do nothing"

    @staticmethod
    def _verify_config(config):
        try:
            return json_to_config(config)
        except KeyError as error:
            key = error.args[0]
            raise ConfigImportError(
                texts.MENU_KEY_ERROR_TITLE,
                texts.MENU_KEY_ERROR_MSG.format(key),
            )
        except ValueError as error:
            # String to int conversion failed.
            string = error.args[0].split("'")[1]
            raise ConfigImportError(
                texts.MENU_VALUE_ERROR_TITLE,
                texts.MENU_VALUE_ERROR_MSG.format(string),
            )

    def _load(self, path):
        try:
            with open(path, 'r') as cfg:
                config_text = cfg.read()
        except FileNotFoundError:
            raise ConfigImportError(
                texts.MENU_FILE_NOT_FOUND_TITLE,
                texts.MENU_FILE_NOT_FOUND_MSG.format(path)
            )

        try:
            config = json.loads(config_text)
        except json.JSONDecodeError:
            raise ConfigImportError(
                texts.MENU_CFG_DECODE_ERROR_TITLE,
                texts.MENU_CFG_DECODE_ERROR_MSG
            )

        config = self._verify_config(config)
        self._context.set_item("config", config)

        self._root.winfo_toplevel().attributes('-topmost', config.toggles.always_top)

    def _handle_import(self, default=False):
        if default:
            path = DEFAULT_CONFIG
        else:
            if self._context.state != States.INITIAL:
                messagebox.showerror(
                    texts.MENU_NOT_ALLOWED_TITLE,
                    texts.MENU_NOT_ALLOWED_MSG
                )
                return
            path = filedialog.askopenfilename(
                defaultextension="*.*",
                filetypes=CFG_ALLOWED_TYPES,
            )

        if not path:
            # Means clicked the cancel
            return

        try:
            self._load(path)
        except ConfigImportError:
            return

        if not default:
            self.__is_config_loaded = True
            # If a new config loaded, set the state to initial
            self._context.state = States.INITIAL

    def _render_file_menu(self, parent):
        file_menu = ttk.Menubutton(parent, text=texts.MENU_CFG_TEXT)
        file_menu.grid(row=0, column=0)

        menu = tk.Menu(file_menu, tearoff=False, activeborderwidth=0)
        file_menu["menu"] = menu

        menu.add_command(
            label=texts.MENU_IMPORT_TEXT, foreground="black",
            command=self._handle_import
        )

        file_menu.menu = menu

    @staticmethod
    def _show_version_info():
        from daily_scrum_tool import __version__ as version
        messagebox.showinfo(
            texts.MENU_VERSION_TEXT,
            "Version: {0}".format(version)
        )

    @staticmethod
    def _show_about_info():
        from daily_scrum_tool import __authors__ as authors
        messagebox.showinfo(
            texts.NAME_PICKER_TITLE,
            texts.ABOUT_TEXT.format(
                title=texts.NAME_PICKER_TITLE,
                authors="\n        ".join(authors),
                tab="    "
            )
        )

    def _render_about_menu(self, parent):
        about_menu = ttk.Menubutton(parent, text=texts.MENU_HELP_TEXT)
        about_menu.grid(row=0, column=1)

        menu = tk.Menu(about_menu, tearoff=False, activeborderwidth=0)
        about_menu["menu"] = menu

        menu.add_command(
            label=texts.MENU_VERSION_TEXT, foreground="black",
            command=self._show_version_info
        )
        menu.add_command(
            label=texts.MENU_ABOUT_TEXT, foreground="black",
            command=self._show_about_info
        )

        about_menu.menu = menu
