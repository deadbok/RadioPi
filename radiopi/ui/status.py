'''
Default status screen.

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
from time import localtime, strftime
from radiopi.log import logger


class Status(object):
    '''
    Class holding the default status screen.
    '''
    id = 'status'
    lcd = None
    lines = ['', '', '', '']
    '''Lines on the LCD.'''

    def __init__(self, lcd):
        '''
        Constructor.

        @param lcd: The interface to LCDd.
        @type lcd: lcdproc.server.Server
        '''
        logger.debug("Creating status screen.")
        self.lcd = lcd
        # Create status screen
        lcd.request('screen_add', self.id)
        lcd.request('screen_set', self.id + ' -priority info')
        # Add lines of text
        self.lcd.request('widget_add', self.id + ' line1 string')
        self.lcd.request('widget_add', self.id + ' line2 string')
        self.lcd.request('widget_add', self.id + ' line3 string')
        self.lcd.request('widget_add', self.id + ' line4 string')

    def update(self):
        '''
        Update the status display.
        '''
        logger.debug("Updating status screen.")
        # Update status line
        self.lines[0] = strftime('%H:%M', localtime())
        # Update custom lines
        for i in range(0, 4):
            self.lcd.request('widget_set', self.id + ' line' + str(i + 1)
                             + ' 1 ' + str(i + 1) + ' "' + self.lines[i]
                             + '"')
