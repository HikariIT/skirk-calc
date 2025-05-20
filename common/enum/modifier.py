from enum import Enum


class ModifierType(Enum):
    ATTACK = 0
    HEALING_BONUS = 1
    REACTION_BONUS = 2
    STAT = 3
    COOLDOWN = 4

class ModifierResult(Enum):
    REJECTED = 0
    APPLIED = 1