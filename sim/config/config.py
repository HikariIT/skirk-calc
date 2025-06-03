from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from common.enum.action import CharacterAction

@dataclass_json
@dataclass
class SimulationConfig:
    character_configs: list[str]
    frame_duration: int = 60 * 20   # 20 seconds
    character_delays: dict[CharacterAction, int] = field(default_factory=CharacterAction.get_default_delays)
    enable_hitlag: bool = True
    seed: int = 0

    @staticmethod
    def from_file(file_path: str) -> 'SimulationConfig':
        with open(file_path, 'r') as f:
            data = f.read()
        return SimulationConfig.from_json(data) # type: ignore

