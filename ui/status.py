'''
Default status screen.

@since: 10/02/2014
@author: oblivion
'''
from time import localtime, strftime
import log


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
        log.logger.debug("Creating status screen.")
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
        log.logger.debug("Updating status screen.")
        # Update status line
        self.lines[0] = strftime('%H:%M', localtime())
        # Update custom lines
        for i in range(0, 4):
            self.lcd.request('widget_set', self.id + ' line' + str(i + 1)
                             + ' 1 ' + str(i + 1) + ' "' + self.lines[i]
                             + '"')
