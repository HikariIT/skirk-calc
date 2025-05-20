# Create common logger using logging library

import logging
import colorlog
import textwrap

import tabulate as tb
from logging import StreamHandler, Formatter, FileHandler

from common.enum.event import LogEventType

tb.PRESERVE_WHITESPACE = True

class Logger:

    LOG_FILE = 'app.log'
    FILE_LOG_LEVEL = logging.DEBUG
    CONSOLE_LOG_LEVEL = logging.INFO
    DEFAULT_LOG_LEVEL = logging.INFO

    def __init__(self, name: str):
        self.logged_events = [
            LogEventType.CHARACTER,
            LogEventType.WEAPON,
            LogEventType.ARTIFACT,
            LogEventType.DAMAGE,
            LogEventType.HEAL,
            LogEventType.ACTION,
            LogEventType.AURA,
            LogEventType.CALCULATION,
            LogEventType.MODIFIER,
            LogEventType.HITLAG,
            # LogEventType.SNAPSHOT,
        ]
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.DEFAULT_LOG_LEVEL)

        # Create console handler
        console_handler = StreamHandler()
        console_handler.setLevel(self.CONSOLE_LOG_LEVEL)
        console_handler.setFormatter(
            colorlog.ColoredFormatter(
                '%(log_color)s%(levelname)s | %(name)20s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'white',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white'
                }
            )
        )
        self.logger.addHandler(console_handler)

        file_handler = FileHandler(self.LOG_FILE)
        file_handler.setLevel(self.FILE_LOG_LEVEL)
        file_formatter = Formatter('%(levelname)s | %(name)20s | %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message: str):
        self._log_wrapped_message(message, self.logger.debug)

    def info(self, message: str):
        self._log_wrapped_message(message, self.logger.info)

    def warning(self, message: str):
        self._log_wrapped_message(message, self.logger.warning)

    def error(self, message: str):
        self._log_wrapped_message(message, self.logger.error)

    def critical(self, message: str):
        self._log_wrapped_message(message, self.logger.critical)

    def _log_wrapped_message(self, message: str, log_function):
        msg = textwrap.fill(message, width=73)
        for line in msg.split('\n'):
            log_function(line)

    def event(self, event_type: LogEventType, target: str, event_name: str, **kwargs):
        if event_type not in self.logged_events:
            return
        table = [
            ['Event'.ljust(15), event_name.ljust(50)],
            ['Type', event_type.name],
            ['Target', target],
            *([key, value] for key, value in kwargs.items())
        ]
        table_str = tb.tabulate(table, headers='firstrow', tablefmt='rounded_grid', maxcolwidths=[20, 50])
        for line in table_str.split('\n'):
            self.logger.info(line.center(15 + 50 + 3))

    def clean_log_file(self):
        with open(self.LOG_FILE, 'w'):
            pass
