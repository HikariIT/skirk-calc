from character.base.character.character import CharacterBase, CharacterWrapper
from profiles.character import CharacterProfile
from common.enum.arkhe import Arkhe
from sim.core.core import Core

from dataclasses import dataclass


@dataclass
class FurinaInternalData:
    fanfare_stacks: int
    max_fanfare_stacks: int
    a4_buffs: list[float]
    a4_interval_reduction: float
    arkhe: Arkhe


class Furina(CharacterBase):
    def __init__(self, core: Core, wrapper: CharacterWrapper, profile: CharacterProfile):
        self._data = FurinaInternalData(
            fanfare_stacks=0,
            max_fanfare_stacks=200,
            a4_buffs=[0.0, 0.0, 0.0],
            a4_interval_reduction=0.0,
            arkhe=Arkhe.OUSIA
        )
        self.clone_wrapper_attributes(wrapper)
        super().__init__(wrapper, core)

        self.energy.max_energy = 60
        self.normal.max_hits = 4
        self.constellation_upgrades.skill = 5
        self.constellation_upgrades.burst = 3
        self.has_arkhe_alignment = True

    def initialize(self):
        self.logger.info("Furina initialized")
        self.logger.info(f"Internal data: {self._data}")
        self.a1()
        self.a4()
        self._a4_tick()
        self._burst_init()

    def elemental_skill(self):
        pass

    def a1(self):
        pass

    def a4(self):
        pass

    def _a4_tick(self):
        pass

    def elemental_burst(self):
        pass

    def _burst_init(self):
        pass
