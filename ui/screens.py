'''
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
from .status import Status
import log


class Screens(object):
    '''
    Class holding the static LCD screens.
    '''
    status = None
    '''Status screen (default screen)'''

    def __init__(self, lcd):
        '''
        Constructor.

        @param lcd: The interface to LCDd.
        @type lcd: lcdproc.server.Server
        '''
        log.logger.debug('Creating screens.')
        self.status = Status(lcd)
