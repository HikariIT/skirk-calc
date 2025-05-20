from base.weapon.weapon import WeaponBase, WeaponWrapper
from sim.core.core import Core
from weapon.fleuve_cendre_ferryman.scalings import FleuveCendreFerrymanScalings


class FleuveCendreFerryman(WeaponBase):
    def __init__(self, wrapper: WeaponWrapper, core: Core) -> None:
        super().__init__(wrapper, core)
        self.scalings = FleuveCendreFerrymanScalings()
        self.logger.info("Fleuve Cendre Ferryman initialized")
