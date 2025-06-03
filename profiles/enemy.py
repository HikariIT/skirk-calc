from dataclasses import dataclass

from common.enum.element import Element


@dataclass
class EnemyProfile:
    level: int
    hp: int
    resists: dict[Element, float]
    particle_drop_threshold: float          # For how many HP lost the enemy will drop particles
    particle_drop_count: int                # How many particles will be dropped when the threshold is reached
    particle_element: Element               # The element of the particles dropped by the enemy
    name: str

    def to_json(self):
        return {
            "level": self.level,
            "hp": self.hp,
            "resists": {element.name: resist for element, resist in self.resists.items()},
            "particle_drop_threshold": self.particle_drop_threshold,
            "particle_drop_count": self.particle_drop_count,
            "particle_element": self.particle_element.name,
            "name": self.name
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            level=data["level"],
            hp=data["hp"],
            resists={Element[element]: resist for element, resist in data["resists"].items()},
            particle_drop_threshold=data["particle_drop_threshold"],
            particle_drop_count=data["particle_drop_count"],
            particle_element=Element[data["particle_element"]],
            name=data["name"]
        )

    def get_default_profile(self):
        return EnemyProfile(
            level=90,
            hp=1000000000,
            resists={element: 0.1 for element in Element},
            particle_drop_threshold=250000,
            particle_drop_count=1,
            particle_element=Element.NONE,  # Default to Pyro particles
            name="Default Enemy"
        )