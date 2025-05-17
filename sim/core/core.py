from common.logger.logger import Logger
from numpy import random


class Core:

    frame: int = 0
    seed: int = 0
    rand: random.Generator
    logger: Logger

