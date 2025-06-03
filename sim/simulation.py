from base.artifact.artifact_set import ArtifactSetBase, ArtifactSetWrapper
from base.character.character import CharacterBase, CharacterWrapper
from base.weapon.weapon import WeaponWrapper
from common.enum.event import Event
from common.enum.heal import HealType
from common.logger.logger import Logger
from common.struct.event.heal import HealEvent
from common.struct.event_data.heal import HealDetails
from profiles.character import CharacterProfile
from sim.config.config import SimulationConfig
from sim.core.core import Core
from sim.core.registry import Registry
from sim.handlers.combat import CombatHandler
from sim.handlers.player import PlayerHandler
from sim.handlers.task import TaskHandler
from sim.handlers.event import EventHandler



class Simulation:

    def __init__(self, cfg: SimulationConfig):
        self.cfg = cfg
        self.logger = Logger(__name__)
        self.logger.clean_log_file()
        self._create_handlers()
        self.registry = Registry()
        self.core = Core(
            self.task_handler,
            self.event_handler,
            self.combat_handler,
            self.player_handler,
            cfg
        )
        self.logger.info(f" Frame: 0 ".center(73, '-'))

    def _create_handlers(self):
        self.task_handler = TaskHandler()
        self.event_handler = EventHandler()

        self.player_handler = PlayerHandler(
            self.event_handler,
            self.task_handler,
            self.cfg.character_delays,
            self.cfg.enable_hitlag
        )

        self.combat_handler = CombatHandler(
            self.event_handler,
            self.task_handler,
            self.player_handler,
            self.cfg.enable_hitlag
        )

    def _add_characters(self):
        for character_config_path in self.cfg.character_configs:
            character, artifact_set = self._initialize_character(character_config_path)
            self.core.player_handler.add_character(character)
            self.core.player_handler.add_artifact_set(artifact_set)

    def _initialize_character(self, cfg_path: str) -> tuple[CharacterBase, ArtifactSetBase]:
        with open(cfg_path, 'r') as f:
            character_profile = CharacterProfile.from_json(f.read()) # type: ignore
            character_wrapper = CharacterWrapper(character_profile, 0, self.logger, self.event_handler, self.task_handler)
            character_constructor = self.registry.get_character(character_wrapper.base.name)
            character = character_constructor(self.core, character_wrapper, character_profile)

            weapon_profile = character_profile.weapon
            weapon_wrapper = WeaponWrapper(weapon_profile, self.logger)
            weapon_constructor = self.registry.get_weapon(weapon_wrapper.base.name)
            weapon = weapon_constructor(weapon_wrapper, self.core)
            character.set_weapon(weapon)

            for set_name, set_count in character_profile.sets.items():
                artifact_set_wrapper = ArtifactSetWrapper(character, set_count)
                artifact_set_constructor = self.registry.get_artifact_set(set_name)
                artifact_set = artifact_set_constructor(artifact_set_wrapper, self.core)

            character.calculate_stats(character_profile)
            return character, artifact_set

    def init(self):
        self._add_characters()

    def run(self):
        for character in self.core.player_handler.get_characters():
            self.logger.info(f"Initializing character: {character.base.name}")
            character.initialize()
        self.furina = self.core.player_handler.get_by_index(0)
        pass

    def tick(self):
        self.logger.info(f" Frame: {self.core.frame + 1} ".center(73, '-'))
        self.core.tick()

        if self.core.frame == 20:
            self.furina.elemental_burst()

    def test_enqueue_tasks(self):
        self.task_handler.add_task('test-task', self._test_task, 5)
        self.task_handler.add_task('test-task2', self._test_task, 5)
        self.task_handler.add_task('test-task3', self._test_task, 5)
        self.task_handler.add_task('test-task4', self._test_task, 10)
        self.task_handler.add_task('test-task5', self._test_task, 20)

    def _test_task(self, *args, **kwargs):
        self.logger.info("Test task executed")
