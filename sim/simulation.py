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
        self.combat_handler = CombatHandler()
        self.player_handler = PlayerHandler()

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
            character.initialize()

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
        heal_details = HealDetails(
            healer_index=3,
            target_index=0,
            heal_bonus=0.0,
            heal_type=HealType.FLAT,
            amount=2137.0,
            name='test-heal'
        )

        self.event_handler.publish(
            Event.ON_HEAL,
            HealEvent(
                data=heal_details,
                target_index=0,
                heal_initial=2137.0,
                heal_final=2137.0 - 420.0,
                heal_overflow=420.0
            )
        )

    def advance_frame(self, frame: int = 0):
        self.logger.info(f" Frame: {self.core.frame + frame} ".center(73, '-'))
        self.core.advance_frame(frame)

        if self.core.frame == 230:
            heal_details = HealDetails(
                healer_index=3,
                target_index=0,
                heal_bonus=0.0,
                heal_type=HealType.FLAT,
                amount=2137.0,
                name='test-heal'
            )
            self.event_handler.publish(
            Event.ON_HEAL,
            HealEvent(
                data=heal_details,
                target_index=0,
                heal_initial=2137.0,
                heal_final=2137.0 - 420.0,
                heal_overflow=420.0
            )
        )

    def test_enqueue_tasks(self):
        self.task_handler.add_task('test-task', self._test_task, 5)
        self.task_handler.add_task('test-task2', self._test_task, 5)
        self.task_handler.add_task('test-task3', self._test_task, 5)
        self.task_handler.add_task('test-task4', self._test_task, 10)
        self.task_handler.add_task('test-task5', self._test_task, 20)

    def _test_task(self, *args, **kwargs):
        self.logger.info("Test task executed")
