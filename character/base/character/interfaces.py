from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from common.struct.character.actions import HealAction
from common.struct.character.result import ActionResult
from common.enum.action import ActionType

T = TypeVar('T')


class CharacterHPInterface(ABC):
    @abstractmethod
    def get_current_hp(self) -> float:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def get_current_hp_percent(self) -> float:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def set_hp(self, hp: float) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def set_hp_percent(self, percent: float) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def modify_hp(self, hp: float) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def modify_hp_percent(self, percent: float) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def heal(self, hp: HealAction) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def drain(self, hp: float) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")


class CharacterDataInterface(Generic[T]):
    _data: T

    def data(self) -> T:
        return self._data


type ActionParams = dict[str, float]


class CharacterActionInterface(ABC):

    @abstractmethod
    def normal_attack(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def charged_attack(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def aimed_shot(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def high_plunge(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def low_plunge(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def elemental_skill(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def elemental_burst(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def dash(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def jump(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def _advance_normal_counter(self) -> None:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def _reset_normal_counter(self) -> None:
        raise NotImplementedError("TODO: This method should be implemented")


class CharacterCheckInterface(ABC):

    @abstractmethod
    def check_action_ready(self, action: ActionType, params: ActionParams) -> bool:
        raise NotImplementedError("TODO: This method should be implemented")


class CharacterBaseInterface(CharacterHPInterface, CharacterDataInterface[T], CharacterActionInterface, CharacterCheckInterface):

    @abstractmethod
    def set_cooldown(self, action: ActionType, frames: int) -> None:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def get_cooldown(self, action: ActionType) -> int:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def reduce_cooldown(self, action: ActionType, frames: int) -> None:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def reset_cooldown(self, action: ActionType) -> None:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def add_energy(self, energy: float) -> None:
        raise NotImplementedError("TODO: This method should be implemented")

    @abstractmethod
    def get_skill_charges(self, action: ActionType) -> int:
        raise NotImplementedError("TODO: This method should be implemented")