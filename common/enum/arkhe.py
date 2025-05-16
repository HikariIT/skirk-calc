from enum import Enum


class Arkhe(Enum):
    OUSIA = 1
    PNEUMA = 2

    def __str__(self):
        return self.name.capitalize()