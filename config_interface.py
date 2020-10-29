"An interface for loading configurations"

import abc


class InterfaceBase(metaclass=abc.ABCMeta):
    "Base class for an interface. Forces for valitadion"
    @abc.abstractmethod
    def validator(self, value):
        "The validator function"

    def __setattr__(self, key, value):
        super().__setattr__(key, self.validator(value))


class PathInterface(InterfaceBase):
    "Includes path information"

    def __init__(self, photos_folder, names_file):
        self.photos = photos_folder
        self.names = names_file

    def validator(self, value):
        "The validator function"
        return str(value)

    def __str__(self):
        return "An interface for storing path informations"


class TextInterface(InterfaceBase):
    "Includes text informations"

    def __init__(self, total_timer_title, individual_timer_title):
        self.total_timer_title = total_timer_title
        self.individual_timer_title = individual_timer_title

    def validator(self, value):
        "The validator function"
        return str(value)

    def __str__(self):
        return "An interface for storing text informations"


class TimeInterface(InterfaceBase):
    "Includes time informations"

    def __init__(self, meeting_time):
        self.meeting_time = meeting_time

    def validator(self, value):
        "The validator function"
        return int(value)

    def __str__(self):
        return "An interface for storing time informations"


class ToogleInterface(InterfaceBase):
    "Includes booleands"

    def __init__(self, each_person_timer, pause_option, always_top):
        self.each_person_timer = each_person_timer
        self.pause_option = pause_option
        self.always_top = always_top 

    def validator(self, value):
        "The validator function"
        return bool(value)

    def __str__(self):
        return "An interface for storing boolean informations"


class ConfigInterface(InterfaceBase):
    "An interface that build entire interfaces"

    def __init__(self, path_inf, text_inf, time_int, toggle_inf):
        self.paths = path_inf
        self.texts = text_inf
        self.times = time_int
        self.toggles = toggle_inf

    def validator(self, value):
        "The validator function"
        if isinstance(value, InterfaceBase):
            return value
        raise ValueError(
            "Given value should be instance of InterfaceBase"
        )

    def __str__(self):
        return "An interface that includes entire interfaces"


def json_to_config(json_config):
    "Converts the json data to ConfigInterface"

    return ConfigInterface(
        PathInterface(
            photos_folder=json_config["photos_folder"],
            names_file=json_config["names_file"]
        ),
        TextInterface(
            total_timer_title=json_config["total_timer_title"],
            individual_timer_title=json_config["timer_for_each_person_title"]
        ),
        TimeInterface(
            meeting_time=json_config["meeting_time"],
        ),
        ToogleInterface(
            each_person_timer=json_config["time_for_each_person"],
            pause_option=json_config["pause_option"],
            always_top=json_config["always_top"]
        )
    )
