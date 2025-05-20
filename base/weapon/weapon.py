from base.weapon.attributes import WeaponBaseAttributes
from dataclasses import dataclass

from base.weapon.scalings import WeaponScalings
from common.enum.stats import CharacterStats
from common.logger.logger import Logger
from profiles.weapon import WeaponProfile
from sim.core.core import Core


class WeaponWrapper:
    base: WeaponBaseAttributes
    scalings: WeaponScalings
    logger: Logger

    def __init__(self, profile: WeaponProfile, logger: Logger) -> None:
        self.base = WeaponBaseAttributes.from_profile(profile)
        self.scalings = WeaponScalings()
        self.logger = logger


class WeaponBase(WeaponWrapper):
    core: Core

    def __init__(self, wrapper: WeaponWrapper, core: Core) -> None:
        self.clone_wrapper_attributes(wrapper)
        self.core = core

    def clone_wrapper_attributes(self, profile: WeaponWrapper) -> None:
        self.base = profile.base
        self.scalings = profile.scalings
        self.logger = profile.logger

    def get_base_atk(self) -> float:
        return self.scalings.get_base_atk()

    def get_main_stat(self) -> tuple[CharacterStats, float]:
        return self.scalings.get_main_stat()