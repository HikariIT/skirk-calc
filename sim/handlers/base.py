from common.logger.logger import Logger


class BaseHandler:

    def __init__(self, logger: Logger, frame: int = 0):
        self.frame = frame
        self.logger = logger
        self.logger.info(f"{self.__class__.__name__} initializing...")

    def tick(self):
        self.frame += 1
