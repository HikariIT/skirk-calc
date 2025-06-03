from enum import Enum


type ActionDict = dict[ActionType, int]


class ActionType(Enum):
    INVALID = 0
    NORMAL = 1
    CHARGED = 2
    HIGH_PLUNGE = 3
    LOW_PLUNGE = 4
    SKILL = 5
    BURST = 6
    AIM = 7
    DASH = 8
    JUMP = 9
    WALK = 10
    WAIT = 11
    SWAP = 12

    @staticmethod
    def get_default_frames(default_frames: int = 0) -> ActionDict:
        return {
            action: default_frames for action in ActionType
        }



class CharacterAction(Enum):
    '''Actions that can be performed by a character and are called in the simulation loop.'''
    SKILL = 1
    BURST = 2
    ATTACK = 3
    CHARGE = 4
    AIM = 5
    DASH = 6
    JUMP = 7
    SWAP = 8

    @staticmethod
    def get_default_delays(default_delay: int = 0) -> dict['CharacterAction', int]:
        return {
            action: default_delay for action in CharacterAction
        }