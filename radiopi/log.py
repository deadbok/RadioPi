'''
Log module.

Copyright 2014 Martin Grønholdt

This file is part of RadioPi.

RadioPi is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RadioPi is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with RadioPi.  If not, see <http://www.gnu.org/licenses/>.
'''
import logging
from logging import handlers
import sys

logger = logging.getLogger("RadioPi")
'''Our Logger object'''

logger.setLevel(logging.DEBUG)

file_log = handlers.RotatingFileHandler("radiopi.log",
                                       maxBytes=10000000,
                                       backupCount=5)
'''Handler for logging to a file.'''

file_log.setLevel(logging.DEBUG)
file_log.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s'))
logger.addHandler(file_log)
file_log.doRollover()

console_log = logging.StreamHandler(sys.stdout)
'''Handler for logging to the console.'''

def init_file_log(level=logging.DEBUG):
    '''
    Initialise the file logging.

    @type level: logging level
    @param level: The level at which the message is logged to the file.
    '''
    file_log.setLevel(level)


class ConsoleFormatter(logging.Formatter):
    def __init__(self):
        logging.Formatter.__init__(self, '%(message)s')

    def format(self, record):
        '''
        Format function to emphasise errors.

        @type record: LogRecord
        @param record: The log record to format.
        @rtype: str
        @return: The resulting string'''
        if record.levelno >= logging.ERROR:
            self._fmt = "%(levelname)s: %(message)s"
            msg = logging.Formatter.format(self, record)
        else:
            self._fmt = "%(message)s"
            msg = logging.Formatter.format(self, record)
        return msg


def init_console_log(level=logging.INFO):
    '''
    Initialise the console logging.

    @type level: logging level
    @param level: The level at which the message is logged to the console.
    '''
    console_log.setLevel(level)
    console_log.setFormatter(ConsoleFormatter())
    logger.addHandler(console_log)

def close_log():
    '''Close all logs.'''
    console_log.close()
    file_log.close()

