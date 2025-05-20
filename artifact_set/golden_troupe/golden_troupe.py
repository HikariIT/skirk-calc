from base.artifact.artifact_set import ArtifactSetBase, ArtifactSetWrapper
from common.enum.stats import CharacterStats
from sim.core.core import Core


class GoldenTroupe(ArtifactSetBase):

    def __init__(self, wrapper: ArtifactSetWrapper, core: Core) -> None:
        super().__init__(wrapper, core)
        self.set_bonus = CharacterStats.get_empty_dict()
        self.logger.info(f"Golden Troupe set initialized with {self.count} pieces.")

        if self.count >= 2:
            self.apply_2pc_bonus()
        if self.count >= 4:
            self.apply_4pc_bonus()

    def apply_2pc_bonus(self):
        pass

    def apply_4pc_bonus(self):
        pass