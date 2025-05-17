from common.enum.weapon import WeaponType
from profiles.weapon import WeaponProfile
from dataclasses import dataclass


@dataclass
class WeaponBaseAttributes:
    name: str
    weapon: WeaponType
    refinement: int
    level: int
    max_level: int

    @staticmethod
    def from_profile(profile: WeaponProfile) -> 'WeaponBaseAttributes':
        return WeaponBaseAttributes(
            profile.name,
            profile.weapon_type,
            profile.refinement,
            profile.level,
            profile.max_level
        )
