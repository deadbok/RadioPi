'''
Generic UI functions

@since 12/02/2014
@author: oblivion
'''
import log
from urllib.parse import urlparse
from lcdproc.client import Client
import sys
from ui.status import Status
from ui.menu import Menu
from ui.menuitem import MenuItem


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
        log.logger.debug("Initialising UI")
        log.logger.info("Connecting to LCDd on " + lcdd_host)
        # Parse the host address
        url = urlparse('//' + lcdd_host)

        hostname = url.hostname
        port = url.port

        # Default to localhost port 13666
        if hostname == None:
            hostname = 'localhost'
        if port == None:
            port = 13666

        log.logger.debug('Hostname: ' + hostname)
        log.logger.debug('Port: ' + str(port))

        try:
            self.lcd = Client(hostname, port)
            self.lcd.request('client_set', '-name RadioPi')
            log.logger.debug('Connection succeeded')
        except OSError as exception:
            log.logger.info('Can not connect to LCDd on ' + lcdd_host)
            log.logger.debug('Exception: ' + str(exception.errno))
            log.logger.debug('Message: ' + exception.strerror)
            sys.exit(1)
        # Initialise UI components
        self.status = Status(self.lcd)
        self.menu = Menu(self.lcd)

    def generate_root_menu(self, players):
        '''
        Generate root menu.

        @param players: Dictionary of players and menu names
        @type players: dict
        '''
        log.logger.debug("Generating root menu")
        items = list()
        # Root menu player entries
        for name in players.keys():
            items.append(MenuItem('', name, True, name))
        # Root Settings menu
        items.append(MenuItem('', 'Settings', True, 'Settings'))

        if len(self.menu.menu) > 0:
            self.menu.delete_menu()
        self.menu.generate_menu('', items)
        self.menu.set_root_menu('')

    def set_event_hook(self, hook):
        '''
        Set the event hook into LCDd.
        '''
        log.logger.debug("Setting event hook to: " + str(hook))
        # Route messages from LCDd to the hook function
        self.lcd.response_hook = hook

    def enter_hook(self):
        '''
        Tell that we are busy in the hook.
        '''
        log.logger.debug('Entering lcd hook')
        self.lcd.hook_busy = True

    def leave_hook(self):
        '''
        Tell that we are ready again.
        '''
        log.logger.debug('Leaving lcd hook')
        self.lcd.hook_busy = False

    def status_update(self, title):
        '''
        Update the status screen.
        '''
        self.status.lines[2] = title
        self.status.update()

    def get_value_from_id(self, id):
        '''
        Get the value of a menu item from the id.
        '''
        return(self.menu.menu[id])
