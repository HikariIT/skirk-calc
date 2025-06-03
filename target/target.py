from common.enum.icd import ICDTag
from sim.core.core import Core

type ICDDict = dict[ICDTag, int]

class Target:

    core: Core
    tags: dict[str, int]
    is_enemy: bool
    is_gadget: bool

    icd_tag_cooldown: tuple[ICDDict, ICDDict, ICDDict, ICDDict]
    icd_tag_counter: tuple[ICDDict, ICDDict, ICDDict, ICDDict]
    icd_damage_tag_cooldown: tuple[ICDDict, ICDDict, ICDDict, ICDDict]
    icd_damage_tag_counter: tuple[ICDDict, ICDDict, ICDDict, ICDDict]

    def __init__(self, core: Core, is_enemy: bool, is_gadget: bool) -> None:
        self.core = core
        self.tags = {}
        self.is_enemy = is_enemy
        self.is_gadget = is_gadget
        self.icd_tag_cooldown = ({}, {}, {}, {})
        self.icd_tag_counter = ({}, {}, {}, {})
        self.icd_damage_tag_cooldown = ({}, {}, {}, {})
        self.icd_damage_tag_counter = ({}, {}, {}, {})