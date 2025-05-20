from base.character.character import CharacterBase
from common.enum.stats import CharacterStatValues, CharacterStats
from common.logger.logger import Logger
from sim.core.core import Core


class ArtifactSetWrapper:
    logger: Logger
    set_bonus: CharacterStatValues
    character_base: CharacterBase
    count: int

    def __init__(self, character: CharacterBase, count: int) -> None:
        self.logger = Logger(__name__[:20])
        self.character = character
        self.set_bonus = CharacterStats.get_empty_dict()
        self.count = count


class ArtifactSetBase:
    core: Core

    def __init__(self, wrapper: ArtifactSetWrapper, core: Core) -> None:
        self.clone_wrapper_attributes(wrapper)
        self.core = core

    def clone_wrapper_attributes(self, wrapper: ArtifactSetWrapper) -> None:
        self.logger = wrapper.logger
        self.character = wrapper.character
        self.set_bonus = wrapper.set_bonus
        self.count = wrapper.count