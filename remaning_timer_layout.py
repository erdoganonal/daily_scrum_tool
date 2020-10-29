"Creates a layout that shows remaning time for each person"

import tkinter as tk

from layout_base import TimerBase
import texts


class RemainingTimerLayout(TimerBase):
    "Creates a layout that shows remaning time for each person"

    def __init__(self, root, context, **grid_options):
        super().__init__(root, context, **grid_options)
        self._remanin_time_label = tk.Label(self.parent)
        self._remanin_time_label.grid(sticky=tk.NSEW)

    @property
    def label(self):
        "returns the label"
        return self._remanin_time_label

    @property
    def is_active(self):
        "Returns true if the component is enabled, false otherwise"
        return self.config.toggles.each_person_timer

    def _funny_timeout(self):
        self.cancel_timer()
        self.label.configure(text=texts.REMAINIG_TIME_FUNNY_TIMEOUT_TEXT)

    def handle_init(self):
        "Set the label text"
        self.label.configure(text=texts.REMAINIG_TIME_INITIAL_BUTTON_TEXT)

    def handle_startup(self):
        "Start the countdown"

        team_size = len(self._context.get_item("names"))
        if self._timer_after_id is None:
            self.countdown(
                label=self.label,
                text_format=self.config.texts.individual_timer_title +
                " {0} m  {1}  s left",
                remaining_time=self.config.times.meeting_time / team_size,
                on_timeout=self._funny_timeout
            )

    def handle_next(self):
        "Cancel timer and start countdown again"
        self.cancel_timer()
        self.handle_startup()

    def handle_reset(self):
        "Cancel timer and set the label text to empty"
        self.cancel_timer()
        self.label.configure(text="")

    def handle_timeout(self):
        "Do nothing"
