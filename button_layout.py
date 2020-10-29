"Creates a layout that allows to operate"

import tkinter as tk

from layout_base import MultiLayoutBase, SingleLayoutBase, States
from constants import PAD, BUTTON_BG, BUTTON_FG
import texts


class StartButtonLayout(SingleLayoutBase):
    "Creates a start button that allows to operate"

    def __init__(self, root, context):
        super().__init__(
            root, context,
            parent=tk.Button(
                root, command=self.click,
                width=int(PAD/2)
            ),
            row=0, column=0,
            sticky=tk.NSEW, pady=(0, PAD)
        )

    def handle_init(self):
        "set the button text to initial value"
        self.parent.configure(
            text=texts.BUTTON_START_TEXT,
            background=BUTTON_BG,
            foreground=BUTTON_FG
        )

    def handle_startup(self):
        "set the button text for choosing the people"
        self.parent.configure(text=texts.BUTTON_CHOOSE_TEXT)

    def handle_next(self):
        "Do nothing"

    def handle_reset(self):
        "set the button text for restarting"
        self.parent.configure(text=texts.BUTTON_RESTART_TEXT)

    def handle_timeout(self):
        "Do nothing"

    def click(self):
        "Action when the button clicked"
        if self._context.state in (States.INITIAL,):
            self._context.state = States.STARTED
        elif self._context.state in (States.RESET,):
            self._context.state = States.INITIAL
        else:
            self._context.state = States.NEXTONE


class PauseButtonLayout(SingleLayoutBase):
    "Creates a pause that allows to manage the time"

    def __init__(self, root, context):
        super().__init__(
            root, context,
            parent=tk.Button(
                root, command=self.click,
                width=int(PAD/2)
            ),
            row=0, column=1,
            sticky=tk.NSEW, pady=(0, PAD), padx=(PAD, 0)
        )

    @property
    def is_active(self):
        "Decides whether the layout active or not"
        return self.config.toggles.pause_option

    def handle_init(self):
        "set the button text and state to initial value"
        self.parent.configure(
            text="Pause",
            background=BUTTON_BG,
            foreground=BUTTON_FG,
            state=tk.DISABLED
        )

    def handle_startup(self):
        "set the button text and state for start-up"
        self.parent.configure(text="Pause", state=tk.NORMAL)

    def handle_next(self):
        "Any next should be act like startup"
        self.handle_startup()

    def handle_reset(self):
        "set the button state"
        self.parent.configure(state=tk.DISABLED)

    def handle_timeout(self):
        "Do nothing"

    def click(self):
        "Action when the button clicked"
        if self._context.state != States.PAUSE:
            self._context.state = States.PAUSE
            self.parent.configure(text="Continue")
        else:
            self._context.set_state_without_invoke(States.NEXTONE)
            self.parent.configure(text="Pause")


class ButtonLayout(MultiLayoutBase):
    "Creates a layout that allows to operate"

    def __init__(self, root, context, **grid_options):
        super().__init__(
            root, context,
            StartButtonLayout, PauseButtonLayout,
            **grid_options
        )
