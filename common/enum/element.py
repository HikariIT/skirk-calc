from enum import Enum


class Element(Enum):
    NONE = 0
    PYRO = 1
    HYDRO = 2
    ELECTRO = 3
    ANEMO = 4
    GEO = 5
    DENDRO = 6
    CRYO = 7

    def __str__(self):
        return self.name.capitalize()