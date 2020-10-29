"Creates a layout that shows remaning time for daily"

import tkinter as tk
from PIL import Image, ImageTk

from layout_base import TimerBase, States
from constants import PAD, LAYOUT_BG, CLOCK_IMAGE_PATH, LABEL_DFT_FG
import texts


class TotalTimerLayout(TimerBase):
    "Displays the remaning time for daily"

    def __init__(self, root, context, **grid_options):
        super().__init__(root, context, **grid_options)

        image = Image.open(CLOCK_IMAGE_PATH)
        resized = image.resize((50, 50), Image.ANTIALIAS)
        clock = ImageTk.PhotoImage(resized)

        # assinged to variable to create strong referance on it
        self._clock = clock

        tk.Label(self.parent, image=clock).grid(
            row=0, column=0, sticky=tk.N
        )

        self._timer_label = tk.Label(self.parent, width=2 * PAD)
        self._timer_label.grid(row=0, column=1, sticky=tk.NS)

    def handle_init(self):
        "On initial, cancel the timer and set the initial text"
        self.cancel_timer()
        self._timer_label.configure(
            text=texts.TOTAL_TMR_INIT_TEXT.format(
                self.config.texts.total_timer_title),
            foreground=LABEL_DFT_FG,
            background=LAYOUT_BG
        )

    def handle_startup(self):
        "On startup, start the timer"
        if self._timer_after_id is not None:
            # A timer still counting
            return

        self.countdown(
            label=self._timer_label,
            text_format=self.config.texts.total_timer_title +
            " Time : {0} m {1} s left",
            remaining_time=self.config.times.meeting_time,
            on_timeout=lambda: setattr(self._context, "state", States.TIMEOUT)
        )

    def handle_reset(self):
        "On reset, cancel the timer"
        self.cancel_timer()

    def handle_next(self):
        "Do nothing"

    def handle_timeout(self):
        "On timeout, set the text"
        self._timer_label.configure(foreground="red")
        self.countup(
            label=self._timer_label,
            text_format=self.config.texts.total_timer_title +
            ": {0} m {1} s elapsed.",
            elapsed_time=0
        )
