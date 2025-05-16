# Create common logger using logging library

import logging
import colorlog
from logging import StreamHandler, Formatter, FileHandler

class Logger:

    LOG_FILE = 'app.log'
    FILE_LOG_LEVEL = logging.DEBUG
    CONSOLE_LOG_LEVEL = logging.INFO
    DEFAULT_LOG_LEVEL = logging.INFO

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.DEFAULT_LOG_LEVEL)

        # Create console handler
        console_handler = StreamHandler()
        console_handler.setLevel(self.CONSOLE_LOG_LEVEL)
        console_handler.setFormatter(
            colorlog.ColoredFormatter(
                '%(log_color)s%(levelname)s | %(name)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white'
                }
            )
        )
        self.logger.addHandler(console_handler)


        file_handler = FileHandler(self.LOG_FILE)
        file_handler.setLevel(self.FILE_LOG_LEVEL)
        file_formatter = Formatter('%(levelname)s | %(name)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)

