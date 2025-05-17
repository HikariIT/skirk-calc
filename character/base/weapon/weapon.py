from character.base.weapon.attributes import WeaponBaseAttributes
from dataclasses import dataclass


@dataclass
class WeaponWrapper:
    base: WeaponBaseAttributes

    @staticmethod
    def from_profile(profile) -> 'WeaponWrapper':
        return WeaponWrapper(
            WeaponBaseAttributes.from_profile(profile)
        )
