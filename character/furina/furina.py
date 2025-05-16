from character.base.character.character import CharacterBase
from common.enum.stats import CharacterStats
from common.enum.element import Element
from common.enum.arkhe import Arkhe
from dataclasses import dataclass
from character.furina.abilities.elemental_skill import salon_solitaire




@dataclass
class FurinaInternalData:
    fanfare_stacks: int
    max_fanfare_stacks: int
    a4_buffs: list[float]
    a4_interval_reduction: float
    arkhe: Arkhe


class Furina(CharacterBase[FurinaInternalData]):
    def __init__(self, name: str, base_info, data: FurinaInternalData, constellation: int = 0):
        super().__init__(name, base_info, data, constellation)
        self.element = Element.HYDRO
        self.arkhe = data.arkhe
        self.fanfare_stacks = data.fanfare_stacks
        self.max_fanfare_stacks = data.max_fanfare_stacks
        self.a4_buffs = data.a4_buffs
        self.a4_interval_reduction = data.a4_interval_reduction

    def elemental_skill(self):
        salon_solitaire(self)

    def a1(self):
        pass

    def a4(self):
        pass
