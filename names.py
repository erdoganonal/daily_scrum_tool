"The list of people who should attend the daily meeting"

import random


class Names:
    "An interface for loading names"

    def __init__(self, source):
        self.__names = None
        self.__backup = None
        self.reload(source)
        self._idx = -1

    def pick_and_remove(self):
        "Pick an item from list and remove that that item from list"
        item = random.choice(self.__names)
        self.__names.remove(item)

        return item

    def pick_one(self):
        "Pick an item from list"
        return random.choice(self.__names)

    def reload(self, source=None):
        "Reloads the list"
        self._idx = -1

        if source is None:
            random.shuffle(self.__backup)
            self.__names = self.__backup.copy()
        else:
            self.__names = self.load(source)
            self.__backup = self.__names.copy()

    def get_next(self):
        "returns the next person name"

        self._idx += 1
        return self.__names[self._idx]

    def __len__(self):
        return len(self.__backup)

    @classmethod
    def load(cls, source, shuffle=True):
        "returns the list of people"
        with open(source) as file:
            names = [line for line in file.readlines() if line.strip()]

        if shuffle:
            random.shuffle(names)

        return names
