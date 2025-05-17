# Simulation - reads config file and creates a new core using config
# Simulation.__init__ accepts ActionList and Core as parameters
#  - sets up Targets in core using A
#  - sets up Characters in core using config
#  - sets up Resonance

# Core, CharacterWrapper, CharacterProfile  -> constructor of Character
# Core, CharacterWrapper, WeaponProfile     -> constructor of Weapon

"""func New(
	p info.CharacterProfile,
	f *int, // current frame
	debug bool, // are we running in debug mode
	log glog.Logger, // logging, can be nil
	events event.Eventter, // event emitter
	tasker task.Tasker,
) (*CharWrapper, error)
"""

from common.logger.logger import Logger
from profiles.character import CharacterProfile
from character.base.character.character import CharacterWrapper
from sim.core.core import Core
from sim.core.registry import CharacterRegistry
from sim.handlers.task import TaskHandler
from sim.pubsub import PubSub

logger = Logger('simulation')
pubsub = PubSub()
task_handler = TaskHandler()
registry = CharacterRegistry()

with open('static/profiles/skirk_mh_eshu.json', 'r') as f:
    profile = CharacterProfile.from_json(f.read()) # type: ignore
    wrapper = CharacterWrapper(profile, 0, logger, pubsub, task_handler)

with open('static/profiles/furina_gt_c2_fcf_ersands.json', 'r') as f:
	profile = CharacterProfile.from_json(f.read()) # type: ignore
	wrapper = CharacterWrapper(profile, 0, logger, pubsub, task_handler)
	core = Core()
	constructor = registry.get_character(wrapper.base.name)
	character = constructor(core, wrapper, profile)
	character.initialize()
