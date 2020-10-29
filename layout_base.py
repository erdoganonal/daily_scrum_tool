"""Base for layout, includes common functions"""

from enum import Enum, auto
import abc

import tkinter as tk
from tkinter import ttk

import constants as const


def _configure(widget):
    properties = {
        "background": const.LAYOUT_BG
    }

    if isinstance(widget, (ttk.Menubutton,)):
        properties.update(font=const.MENU_BTN_FONT)
        style = ttk.Style(widget)
        style.configure(widget.winfo_class(), **properties)
        return
    if isinstance(widget, (tk.Button)):
        widget.configure(
            font=const.BUTTON_FONT,
            background=const.BUTTON_BG
        )
        return
    if isinstance(widget, (tk.Label)):
        widget.configure(font=const.LABEL_DFT_FONT)
        widget.configure(fg=const.LABEL_DFT_FG)
    widget.configure(**properties)


def configure(widget):
    "Set some configurations for given widget and its children"
    _configure(widget)
    for child in widget.winfo_children():
        configure(child)


class LayoutBase:
    "Base for all layouts"
    def __init__(self, root, context, parent=None, **grid_options):
        self._root = root
        self._context = context
        if parent is None:
            self.parent = tk.Frame(root)
        else:
            self.parent = parent
        self._grid_options = grid_options

    @property
    def config(self):
        "returns the configurations"
        return self._context.get_item("config")

    @property
    def is_active(self):
        """If returns a True value, all handlers will be triggered,
                        False value, only handle_reset will be triggered.
        """
        # Assume that all interfaces is active if they are registered
        return True

    def place(self):
        "Places the widget with given options"
        self.parent.grid(**self._grid_options)

    def place_forget(self):
        "Removes the wigdet"
        self.parent.grid_forget()


class SingleLayoutBase(LayoutBase, metaclass=abc.ABCMeta):
    "Base for single layouts"

    @abc.abstractmethod
    def handle_init(self):
        "Call when the state is set to INITIAL"

    @abc.abstractmethod
    def handle_startup(self):
        "Call when the state is set to STARTED"

    @abc.abstractmethod
    def handle_next(self):
        "Call when the state is set to NEXTONE"

    @abc.abstractmethod
    def handle_reset(self):
        "Call when the state is set to RESET"

    @abc.abstractmethod
    def handle_timeout(self):
        "Call when the state is set to TIMEOUT"


class MultiLayoutBase(LayoutBase):
    "Base for multiple layouts"
    def __init__(self, root, context, *layouts, **grid_options):
        super().__init__(root, context, **grid_options)
        self._layouts = layouts

        for layout in self._layouts:
            context.register(layout(self.parent, context))


# TimerBase is an abstract class. No instance should be created from it.
# pylint: disable=abstract-method
class TimerBase(SingleLayoutBase):
    "Base for timer based layouts."

    def __init__(self, root, context, **grid_options):
        super().__init__(root, context, **grid_options)
        self._timer_after_id = None

    def cancel_timer(self):
        "Cancels the countdown"
        if self._timer_after_id is not None:
            self._root.after_cancel(self._timer_after_id)

        self._timer_after_id = None

    def countdown(self, label, text_format, remaining_time, on_timeout=None):
        "Starts the countdown"
        minutes = int(remaining_time / 60)
        seconds = int(remaining_time % 60)

        if (minutes + 60 * seconds) <= 0:
            if callable(on_timeout):
                on_timeout()
            return

        if not self._context.state == States.PAUSE:
            label.configure(text=text_format.format(minutes, seconds))
            remaining_time -= 1

        self._timer_after_id = self._root.after(1000, lambda: self.countdown(
            label, text_format, remaining_time, on_timeout
        ))

    def countup(self, label, text_format, elapsed_time=0):
        "Starts the countup"
        minutes = int(elapsed_time / 60)
        seconds = int(elapsed_time % 60)

        if not self._context.state == States.PAUSE:
            label.configure(text=text_format.format(minutes, seconds))
            elapsed_time += 1

        self._timer_after_id = self._root.after(1000, lambda: self.countup(
            label, text_format, elapsed_time
        ))


class States(Enum):
    "Enum values for context state"

    INITIAL = auto()
    STARTED = auto()
    NEXTONE = auto()
    TIMEOUT = auto()
    PAUSE = auto()
    RESET = auto()


class LayoutContext:
    "A context that includes entire layouts"

    def __init__(self):
        self._attributes = []
        self._state = States.INITIAL
        self._globals = {}

    @property
    def state(self):
        "return the state of the context"
        return self._state

    @state.setter
    def state(self, new_state):
        "set the of the context, and call related functions"
        if not isinstance(new_state, States):
            raise ValueError("new state should be value of States")

        self._state = new_state

        for layout in self:
            # Always allow initial step

            if layout.is_active:
                layout.place()
            else:
                # If a component is not active,
                # no need to trigger handlers
                layout.place_forget()
                continue

            if isinstance(layout, MultiLayoutBase):
                # If a layout contains multiple instances,
                # no need to trigger the handlers.
                # Trigger sub of layouts is enough.
                continue

            if new_state == States.INITIAL:
                layout.handle_init()
            elif new_state == States.STARTED:
                layout.handle_startup()
            elif new_state == States.NEXTONE:
                layout.handle_next()
            elif new_state == States.TIMEOUT:
                layout.handle_timeout()
            elif new_state == States.RESET:
                layout.handle_reset()

            if self._state != new_state:
                # If state does not equal the state that was set, means
                # that the state changed during iteration. If a new state set,
                # the loop needs to break to not override other state change.
                break

    def set_state_without_invoke(self, state):
        "Set the state without invoking handlers"
        self._state = state

    def __iter__(self):
        for item in self._attributes:
            yield item

    def get_item(self, name):
        "Add an item to the context to use it from another layouts"
        return self._globals[name]

    def set_item(self, name, value):
        "return the item from context which set before"
        self._globals[name] = value

    def del_item(self, name):
        "remove an item from context"
        del self._globals[name]

    def register(self, *args):
        "add given layouts in the context"
        for arg in args:
            if not isinstance(arg, (SingleLayoutBase, MultiLayoutBase)):
                raise TypeError("{0} should be instance of SingleLayoutBase".format(
                    arg.__class__.__name__
                ))

            self._attributes.append(arg)
