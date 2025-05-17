from typing import TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')  # Represents the type of the weapon's internal data


class BaseWeaponInterface(ABC, Generic[T]):

    @abstractmethod
    def __init__(self, data: T):
        pass