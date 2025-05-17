from abc import ABC, abstractmethod

from common.struct.character.actions import HealAction
from common.struct.character.result import ActionResult
from common.enum.action import ActionType


class CharacterHPInterface(ABC):

    def get_current_hp(self) -> float:
        raise NotImplementedError("TODO: This method should be implemented")

    def get_current_hp_percent(self) -> float:
        raise NotImplementedError("TODO: This method should be implemented")

    def set_hp(self, hp: float) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    def set_hp_percent(self, percent: float) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    def modify_hp(self, hp: float) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    def modify_hp_percent(self, percent: float) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    def heal(self, hp: HealAction) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    def drain(self, hp: float) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")


type ActionParams = dict[str, float]


class CharacterActionInterface(ABC):

    def normal_attack(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    def charged_attack(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    def aimed_shot(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    def high_plunge(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    def low_plunge(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    def elemental_skill(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    def elemental_burst(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    def dash(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    def jump(self, params: ActionParams) -> ActionResult:
        raise NotImplementedError("TODO: This method should be implemented")

    def _advance_normal_counter(self) -> None:
        raise NotImplementedError("TODO: This method should be implemented")

    def _reset_normal_counter(self) -> None:
        raise NotImplementedError("TODO: This method should be implemented")


class CharacterCheckInterface:

    def check_action_ready(self, action: ActionType, params: ActionParams) -> bool:
        raise NotImplementedError("TODO: This method should be implemented")


class CharacterBaseInterface(CharacterHPInterface, CharacterActionInterface, CharacterCheckInterface):


    def set_cooldown(self, action: ActionType, frames: int) -> None:
        raise NotImplementedError("TODO: This method should be implemented")


    def get_cooldown(self, action: ActionType) -> int:
        raise NotImplementedError("TODO: This method should be implemented")

    def reduce_cooldown(self, action: ActionType, frames: int) -> None:
        raise NotImplementedError("TODO: This method should be implemented")

    def reset_cooldown(self, action: ActionType) -> None:
        raise NotImplementedError("TODO: This method should be implemented")

    def add_energy(self, energy: float) -> None:
        raise NotImplementedError("TODO: This method should be implemented")

    def get_skill_charges(self, action: ActionType) -> int:
        raise NotImplementedError("TODO: This method should be implemented")