from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class TalentProfile:
    attack: int
    skill: int
    burst: int

    @staticmethod
    def get_kqms() -> 'TalentProfile':
        return TalentProfile(9, 9, 9)