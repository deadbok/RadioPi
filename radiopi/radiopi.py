'''
Main file for RadioPi class.

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
import optparse
from radiopi.log import init_file_log, init_console_log, logger, close_log
import logging
from radiopi.players.players import Players
from radiopi.ui.ui import UI
from radiopi.sm import StateMachine
from radiopi import __version__

# VERSION = '0.2'
# '''The current version.'''


class RadioPi(object):
    '''
    Main class for RadioPi
    '''
    players = None
    '''An dictionary of all players. These are presented at the top level menu
    by their key.'''
    ui = None
    '''All UI stuff.'''
    current_player = None
    '''The current player.'''
    loops = 0
    '''Counter to tell how many times we've been in the main loop.'''
    state_machine = None
    '''The state machine directing the main loop.'''
    current_event = ''
    '''The current event that we are handling.'''
    def __init__(self):
        '''
        Constructor. Handles command line parsing, and initialisation of
        everything.
        '''
        # Parse command line
        usage = "usage: %prog [options] lcd_host[:port] mpd_host[:port]"
        arg_parser = optparse.OptionParser(usage=usage)
        arg_parser.add_option("-v", "--verbose",
                              action="store_true", dest="verbose",
                              default=False,
                              help="Print detailed progress")
        arg_parser.add_option("-q", "--quiet",
                              action="store_true", dest="quiet",
                              default=False,
                              help="Only print errors")
        arg_parser.add_option("-l", "--log-level",
                              type="int", default=2,
                              help="Set the logging level for the log files (0-5)"
                              )
        (options, args) = arg_parser.parse_args()

        if options.log_level == 0:
            init_file_log(logging.NOTSET)
        elif options.log_level == 1:
            init_file_log(logging.DEBUG)
        elif options.log_level == 2:
            init_file_log(logging.INFO)
        elif options.log_level == 3:
            init_file_log(logging.WARNING)
        elif options.log_level == 4:
            init_file_log(logging.ERROR)
        elif options.log_level == 5:
            init_file_log(logging.CRITICAL)
        else:
            init_file_log(logging.INFO)
        if options.verbose:
            init_console_log(logging.DEBUG)
        elif options.quiet:
            init_console_log(logging.ERROR)
        else:
            init_console_log()

        logger.info("RadioPi V" + __version__)

        # Hostname for LCDd
        lcd_host = "localhost"
        if len(args) > 0:
            lcd_host = args[0]
        # Hostname for mpd
        mpd_host = "localhost"
        if len(args) > 1:
            mpd_host = args[1]

        # Initialise players
        self.players = Players(mpd_host)
        # Initialise UI
        self.ui = UI(lcd_host)
        self.ui.generate_root_menu(self.players.players)
        self.ui.set_event_hook(self.event_hook)
        # Initialise the state machine
        self.state_machine = StateMachine()
        # Add states
        self.state_machine.create_state('default_update', self.default_update)
        self.state_machine.set_default('default_update')
        self.state_machine.create_state('leave_menu', self.leave_menu)
        self.state_machine.create_state('select', self.select)
        self.state_machine.create_state('enter_menu', self.enter_menu)
        self.state_machine.create_state('up', self.up)
        self.state_machine.create_state('down', self.down)
        self.state_machine.create_state('enter', self.enter)

    def default_update(self):
        '''
        Default state to run when there's nothing much to do. Updates the
        status screen and polls LCDd for messages.
        '''
        # Do not update display every time
        # Would be better with another solution, like a separate thread
        if self.loops == 1000000:
            self.loops = 0
            title = ''
            # Get the current title if any
            if not self.current_player == None:
                title = self.current_player.get_playing()
            self.ui.status_update(title)
        # Poll the lcd for messages
        self.ui.lcd.poll()
        # Increase the loop counter
        self.loops += 1

    def enter_menu(self):
        '''
        Run by the state machine when the lcd says a menu has been entered.
        '''
        # Root menu
        if self.current_event == '""' or self.current_event == '_client_menu_':
            return()
        # Check if it is one of the player menus
        if self.current_event in self.players.players.keys():
            # Save the player
            self.current_player = self.players.players[self.current_event]
            # Get the menu
            items = self.current_player.get_menu('', self.current_event)
            self.ui.enter_menu(self.current_event, items)
            return()
        # If none of the above, we are dealing with an item specific to the
        # current player.
        value = self.ui.get_value_from_id(self.current_event)
        items = self.current_player.get_menu(value, self.current_event)
        self.ui.enter_menu(self.current_event, items)

    def leave_menu(self):
        '''
        Run by the state machine when the lcd says a menu has been left.
        '''
        pass

    def select(self):
        '''
        Something has been selected. If the value is a list, play it, else it
        is a string of the menu item selected.
        '''
        # If there is no player, bail out
        if self.current_player == None:
            return

        value = self.ui.get_value_from_id(self.current_event)
        self.current_player.select(value)

    def up(self):
        '''
        Up button pressed. Send to the current player.
        '''
        if not self.current_player == None:
            self.current_player.up()

    def down(self):
        '''
        Down button pressed. Send to the current player.
        '''
        if not self.current_player == None:
            self.current_player.down()

    def enter(self):
        '''
        Enter button is pressed enter player menu or root menu.
        '''
        if self.current_player == None:
            self.ui.menu.goto('')
        else:
            self.ui.menu.goto(self.current_player.name)

    def main_loop(self):
        '''
        This is the main loop where the state machine is started.
        '''
        # Initial paint of the status screen
        self.ui.status.update()
        while(1):
            self.state_machine.next_state()

    def event_hook(self, event):
        '''
        Handle events from the UI.

        @param event: The message from from LCDd.
        @type event: String.
        '''
        # Tell that we are busy
        self.ui.enter_hook()

        event = event.strip('\n')
        logger.debug("Event: " + event)
        # Process menu events
        if 'menuevent' in event:
            event = event.replace('menuevent ', '')
            # A menu has been entered
            if 'enter' in event:
                self.current_event = event.replace('enter ', '')
                self.state_machine.queue_state('enter_menu')
            # Something has been selected
            if 'select' in event:
                self.current_event = event.replace('select ', '')
                # Ignore back button
                if not 'back' in self.current_event:
                    self.state_machine.queue_state('select')
            # The menu has been left
            if 'leave' in event:
                self.current_event = event.replace('leave ', '')
                self.state_machine.queue_state('leave_menu')
        # Key press
        if 'key' in event:
            event = event.replace('key', '')
            # Save the event
            self.current_event = event
            # Up key
            if 'Up' in event:
                self.state_machine.queue_state('up')
            # Down key
            if 'Down' in event:
                self.state_machine.queue_state('down')
            # Enter key
            if 'Enter' in event:
                self.state_machine.queue_state('enter')
        # Tell that we're done
        self.ui.leave_hook()
