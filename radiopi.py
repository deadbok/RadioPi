'''
Main file for RadioPi, an interface between various programs and an LCD, to
function as a sort of portable radio/media player.

@since 09/02/2014
@author: oblivion
'''
import optparse
import log
import logging
from players.players import Players
from ui.ui import UI
from time import sleep
from sm import StateMachine

VERSION = '0.1'


class RadioPi(object):
    '''
    Main class for RadioPi
    '''
    players = None
    '''All players.'''
    ui = None
    '''All UI stuff.'''
    current_player = None
    '''Current player.'''
    loops = 0
    '''Counter to tell how many times we've been in the main loop.'''
    state_machine = None
    '''The state machine directing the main loop.'''
    current_event = ''
    '''The current event that we are handling.'''
    def __init__(self):
        '''
        Constructor.
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
            log.init_file_log(logging.NOTSET)
        elif options.log_level == 1:
            log.init_file_log(logging.DEBUG)
        elif options.log_level == 2:
            log.init_file_log(logging.INFO)
        elif options.log_level == 3:
            log.init_file_log(logging.WARNING)
        elif options.log_level == 4:
            log.init_file_log(logging.ERROR)
        elif options.log_level == 5:
            log.init_file_log(logging.CRITICAL)
        else:
            log.init_file_log(logging.INFO)
        if options.verbose:
            log.init_console_log(logging.DEBUG)
        elif options.quiet:
            log.init_console_log(logging.ERROR)
        else:
            log.init_console_log()

        log.logger.info("RadioPi V" + VERSION)

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
        self.state_machine.create_state('play', self.play)
        self.state_machine.create_state('enter_menu', self.enter_menu)

    def default_update(self):
        '''
        Default update state to run when there's nothing much to do.
        '''
        # Do not update display every time
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
        Run when the lcd says a menu has been entered.
        '''
        # Check if it is one of the player menus
        if self.current_event in self.players.players.keys():
            # Save the player
            self.current_player = self.players.players[self.current_event]
            self.ui.menu.enter(self.current_event,
                               self.current_player.get_items('/'))

    def leave_menu(self):
        '''
        Run when the lcd says a menu has been left.
        '''
        # Clear the menu if it needs to
        self.ui.menu.leave(self.current_event)

    def play(self):
        '''
        Play something if its the right thing to do.
        '''
        # Add to playlist
        self.current_player.add_item(self.current_event)
        # Start playing if stopped
        if not self.current_player.playing:
            self.current_player.play()
            self.status_update()

    def main_loop(self):
        # Initial paint of the status screen
        self.ui.status.update()
        while(1):
            self.state_machine.next_state()

    def event_hook(self, event):
        '''
        Handle events from the UI.
        '''
        # Tell that we are busy
        self.ui.enter_hook()

        event = event.strip('\n')
        log.logger.debug("Event: " + event)
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
                    self.state_machine.queue_state('play')
            # The menu has been left
            if 'leave' in event:
                self.current_event = event.replace('leave ', '')
                self.state_machine.queue_state('leave_menu')
        # Tell that we're done
        self.ui.leave_hook()


def main():
    radiopi = RadioPi()
    radiopi.main_loop()

if __name__ == '__main__':
    main()
