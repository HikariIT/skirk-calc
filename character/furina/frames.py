from common.enum.action import ActionType, ActionDict


class FurinaFrames:

    def __init__(self):
        self.burst = ActionType.get_default_frames(121)
        self.burst[ActionType.NORMAL] = 113
        self.burst[ActionType.CHARGED] = 113
        self.burst[ActionType.SKILL] = 114
        self.burst[ActionType.DASH] = 115
        self.burst[ActionType.JUMP] = 115
        self.burst[ActionType.SWAP] = 111

    def get_burst_frames(self, next_action: ActionType) -> int:
        return self.burst[next_action]