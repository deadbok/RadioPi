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
    screen = None
    '''LCDd screen.'''
    widgets = [None, None, None, None]
    '''Widgets on the screen.'''
    lines = ['', '', '', '']
    '''Lines on the LCD.'''

    def __init__(self, lcd):
        '''
        Constructor.

        @param lcd: The interface to LCDd.
        @type lcd: lcdproc.server.Server
        '''
        log.logger.debug("Creating status screen.")
        # Create status screen
        self.screen = lcd.add_screen('status')
        self.screen.set_priority('info')
        # Add lines of text
        self.widgets[0] = self.screen.add_string_widget('sys_status', y=1)
        self.widgets[1] = self.screen.add_string_widget('line1', y=2)
        self.widgets[2] = self.screen.add_string_widget('line2', y=3)
        self.widgets[3] = self.screen.add_string_widget('line3', y=4)

    def update(self):
        '''
        Update the status display.
        '''
        log.logger.debug("Updating status screen.")
        # Update status line
        self.lines[0] = strftime('%H:%M', localtime())
        # Update custom lines
        for i in range(0, 4):
            self.widgets[i].set_text(self.lines[i])
            self.widgets[i].update()
