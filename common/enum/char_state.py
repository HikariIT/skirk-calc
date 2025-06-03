from enum import Enum


class CharacterState(Enum):
    NONE = 0
    IDLE = 1
    NORMAL_ATTACK = 2
    CHARGE_ATTACK = 3
    PLUNGE_ATTACK = 4
    SKILL = 5
    BURST = 6
    AIM = 7
    DASH = 8
    JUMP = 9
    WALK = 10
    SWAP = 11