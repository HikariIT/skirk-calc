from base.character.character import CharacterBase, CharacterWrapper
from common.enum.stats import CharacterStats, CharacterStatValues
from character.furina.scalings import FurinaScalings
from common.struct.event_data.heal import HealDetails
from common.struct.event.heal import HealEvent
from common.enum.event import Event
from common.enum.arkhe import Arkhe
from common.enum.heal import HealType
from common.const.const import HEAL_ALL_TARGETS

from profiles.character import CharacterProfile
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
        self.scalings = FurinaScalings()
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

    # When the active character in your party receives healing, if the source of the healing is not Furina herself
    # and the healing overflows, then Furina will heal nearby party members for 2% of their Max HP once every 2s
    # within the next 4s.
    def a1(self):
        if self.base.ascension < 1:
            return
        self.core.event_handler.subscribe(
            Event.ON_HEAL,
            self._a1_callback,
            'furina-a1'
        )

    def _a1_callback(self, *args, **kwargs):
        heal_event: HealEvent = args[0]
        if heal_event.data.healer_index == self.index:
            return
        if heal_event.target_index != self.core.player_handler.active:
            return
        if heal_event.heal_overflow <= 0:
            return
        if not self.modifier_handler.has_status_active('furina-a1-hot'):
            self.core.task_handler.add_task('furina-a1-hot-instance1', self._a1_heal, 2 * 60)

        self.modifier_handler.add_status('furina-a1-hot', 4 * 60, False)

    def _a1_heal(self, *args, **kwargs):
        if not self.modifier_handler.has_status_active('furina-a1-hot'):
            return
        self.core.player_handler.heal(
            HealDetails(
                healer_index=self.index,
                target_index=HEAL_ALL_TARGETS,
                heal_type=HealType.PERCENTAGE,
                amount=0.02,
                heal_bonus=0.0,
                name='furina-a1-hot',
            )
        )

        self.core.task_handler.add_task('furina-a1-hot-instance2', self._a1_heal, 2 * 60)


    def a4(self):
        pass

    def _a4_tick(self):
        pass

    def elemental_burst(self):
        pass

    def _burst_init(self):
        pass

    def get_base_stats(self) -> CharacterStatValues:
        return {
            CharacterStats.BASE_ATK: self.scalings.get_base_atk(),
            CharacterStats.BASE_HP: self.scalings.get_base_hp(),
            CharacterStats.BASE_DEF: self.scalings.get_base_def(),
        }