'''
Generic UI functions

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
from radiopi.log import logger
from urllib.parse import urlparse
from radiopi.lcdproc.client import Client
from radiopi.ui.status import Status
from radiopi.ui.menu import Menu


class UI(object):
    '''
    classdocs
    '''
    lcd = None
    status = None
    menu = None

    def __init__(self, lcdd_host):
        '''
        Constructor
        '''
        logger.debug("Initialising UI")
        logger.info("Connecting to LCDd on " + lcdd_host)
        # Parse the host address
        url = urlparse('//' + lcdd_host)

        hostname = url.hostname
        port = url.port

        # Default to localhost port 13666
        if hostname == None:
            hostname = 'localhost'
        if port == None:
            port = 13666

        logger.debug('Hostname: ' + hostname)
        logger.debug('Port: ' + str(port))

        self.lcd = Client(hostname, port)
        self.lcd.request('client_set', '-name RadioPi')
        logger.debug('Connection succeeded')

        # Initialise UI components
        self.status = Status(self.lcd)
        self.menu = Menu(self.lcd)
        self.reserve_keys()

    def reserve_keys(self):
        '''Reserve keys for use during playback.'''
        self.lcd.request('client_add_key', 'Up')
        self.lcd.request('client_add_key', 'Down')
        self.lcd.request('client_add_key', 'Enter')

    def generate_root_menu(self, players):
        '''
        Generate root menu.

        @param players: Dictionary of players and menu names
        @type players: dict
        '''
        # The root menu is not saved in the internal dict, and therefore it is
        # never deleted
        logger.debug("Generating root menu")
        # Root menu player entries
        for name in players.keys():
            self.lcd.request('menu_add_item', '"" "' + name + '" menu "'
                             + name + '"')
        # Root Settings menu
        self.lcd.request('menu_add_item', '"" "Settings" menu "Settings"')
        # Back
        self.lcd.request('menu_add_item', '"" "back" action "< Back"')
        self.lcd.request('menu_set_item', '"" back -menu_result quit')
        # Set as root menu
        self.menu.set_root('')

    def set_event_hook(self, hook):
        '''
        Set the event hook into LCDd.
        '''
        logger.debug("Setting event hook to: " + str(hook))
        # Route messages from LCDd to the hook function
        self.lcd.response_hook = hook

    def enter_hook(self):
        '''
        Tell that we are busy in the hook.
        '''
        logger.debug('Entering lcd hook')
        self.lcd.hook_busy = True

    def leave_hook(self):
        '''
        Tell that we are ready again.
        '''
        logger.debug('Leaving lcd hook')
        self.lcd.hook_busy = False

    def status_update(self, title):
        '''
        Update the status screen.
        '''
        self.status.lines[2] = title
        self.status.update()

    def get_value_from_id(self, _id):
        '''
        Get the value of a menu item from the id.
        '''
        return(self.menu.menu[_id.strip()].value)

    def enter_menu(self, root, items):
        '''
        A menu has been selected.
        '''
        self.menu.generate(root, items)

    def close(self):
        '''Close the connection to LCDd.'''
        if not self.lcd == None:
            self.lcd.close()
