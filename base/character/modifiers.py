from copy import copy
from common.enum.event import LogEventType
from common.enum.modifier import ModifierType
from common.logger.logger import Logger
from common.struct.modifier.attack import CharacterAttackModifier
from common.struct.modifier.modifier import BaseModifier
from common.struct.modifier.status import CharacterStatusModifier
from common.struct.modifier.healing_bonus import IncomingHealingBonusModifier

class ModifierHandler:
    status_list: dict[str, CharacterStatusModifier]
    modifiers: dict[ModifierType, dict[str, BaseModifier]]

    def __init__(self, frame, logger: Logger, character_name: str):
        self.status_list = {}
        self.modifiers = {
            ModifierType.HEALING_BONUS: {},
            ModifierType.REACTION_BONUS: {},
            ModifierType.STAT: {},
            ModifierType.ATTACK: {},
            ModifierType.COOLDOWN: {},
        }
        self.frame = frame
        self.logger = logger
        self.name = character_name

    def add_status(self, status_key: str, frame_duration: int, hitlag: bool) -> None:
        status = CharacterStatusModifier(status_key, frame_duration, hitlag)
        status.update_expiry(self.frame)
        if status_key in self.status_list:
            old_status = self.status_list[status_key]
            if old_status.status_expiry > self.frame:
                self._update_status(copy(old_status), status)
                return

        self._create_status(status)

    def delete_status(self, status_key: str) -> None:
        if status_key in self.status_list:
            status = self.status_list[status_key]
            self._trigger_status_expiry(status)
            del self.status_list[status_key]

    def add_incoming_healing_bonus_modifier(self, modifier: IncomingHealingBonusModifier) -> None:
        self.modifiers[ModifierType.HEALING_BONUS][modifier.status_key] = modifier
        self.logger.event(
            LogEventType.MODIFIER,
            self.name,
            'modifier-added-healing-bonus',
            status_key=modifier.status_key,
            frame_duration=modifier.frame_duration,
            hitlag=modifier.hitlag,
            status_expiry=modifier.status_expiry,
            status_extension=modifier.status_extension,
            frame=self.frame,
        )

    def add_reaction_bonus_modifier(self, status_key: str, frame_duration: int) -> None:
        ...

    def add_stat_modifier(self, status_key: str, frame_duration: int) -> None:
        ...

    def add_attack_modifier(self, modifier: CharacterAttackModifier) -> None:
        self.modifiers[ModifierType.ATTACK][modifier.status_key] = modifier
        self.logger.event(
            LogEventType.MODIFIER,
            self.name,
            'modifier-added-attack',
            status_key=modifier.status_key,
            frame_duration=modifier.frame_duration,
            hitlag=modifier.hitlag,
            status_expiry=modifier.status_expiry,
            status_extension=modifier.status_extension,
            frame=self.frame,
        )

    def add_cooldown_modifier(self, status_key: str, frame_duration: int) -> None:
        ...

    def get_healing_bonus(self) -> float:
        return sum(
            modifier.value for modifier in self.modifiers[ModifierType.HEALING_BONUS].values()
            if modifier.status_expiry > self.frame
        )

    def get_remaining_status_duration(self, status_key: str) -> int:
        if status_key in self.status_list:
            return max(0, self.status_list[status_key].status_expiry - self.frame)
        return 0

    def has_status_active(self, status_key: str) -> bool:
        return status_key in self.status_list and self.status_list[status_key].status_expiry > self.frame

    def _create_status(self, status: CharacterStatusModifier) -> None:
        self.status_list[status.status_key] = status
        self.logger.event(
            LogEventType.MODIFIER,
            self.name,
            'status-added',
            status_key=status.status_key,
            expiry=status.status_expiry,
            frame=self.frame,
        )

    def _update_status(self, old_status: CharacterStatusModifier, new_status: CharacterStatusModifier) -> None:
        old_expiry = old_status.status_expiry
        old_status.status_expiry = self.frame + new_status.frame_duration
        self.status_list[old_status.status_key] = old_status
        self.logger.event(
            LogEventType.MODIFIER,
            self.name,
            'status-refreshed',
            status_key=old_status.status_key,
            expiry_old=old_expiry,
            expiry_new=old_status.status_expiry,
            frame=self.frame,
        )

    def _trigger_status_expiry(self, status: CharacterStatusModifier) -> None:
        if status.status_expiry <= self.frame:
            self.logger.event(
                LogEventType.MODIFIER,
                self.name,
                'status-expired',
                status_key=status.status_key,
                expiry=status.status_expiry,
                frame=self.frame,
            )
            del self.status_list[status.status_key]

    def _trigger_modifier_expiry(self, modifier: BaseModifier) -> None:
        for modifier_key in self.modifiers:
            for key, mod in self.modifiers[modifier_key].items():
                if mod.status_expiry <= self.frame:
                    self.logger.event(
                        LogEventType.MODIFIER,
                        self.name,
                        f'modifier-expired-{modifier_key.name.lower().replace("_", "-")}',
                        status_key=mod.status_key,
                        expiry=mod.status_expiry,
                        frame=self.frame,
                    )
                    del self.modifiers[modifier_key][key]

    def tick(self) -> None:
        self.frame += 1
        for status_key in list(self.status_list.keys()):
            status = self.status_list[status_key]
            self._trigger_status_expiry(status)