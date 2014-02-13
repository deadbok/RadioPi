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

VERSION = '0.1'


class RadioPi(object):
    '''
    Main class for RadioPi
    '''
    players = None
    ui = None
    menu_items = list()
    menu_name = ''

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

    def main_loop(self):
        while(1):
            # self.ui.status.update()
            self.ui.lcd.poll()
            # print('.', end='')

    def event_hook(self, event):
        '''
        Handle events from the UI.
        '''
        event = event.strip('\n')
        log.logger.debug("Event: " + event)
        # Process menu events
        if 'menuevent' in event:
            event = event.replace('menuevent ', '')
            # A menu has been entered
            if 'enter' in event:
                event = event.replace('enter ', '')
                # Check if it is one of the player menus
                if event in self.players.players.keys():
                    self.menu_items = self.players.players[event].get_items('/')
                    self.ui.menu.generate_selection_list(event, self.menu_items)
                    self.menu_name = event
            # Something has been selected
            if 'select' in event:
                event = event.replace('select ', '')
                print(self.menu_items[int(event)])
            # The menu has been left
            if 'leave' in event:
                event = event.replace('leave ', '')
                # Clear the menu if it is dynamic
                if event == self.menu_name:
                    self.ui.menu.delete_selection_list(event, self.menu_items)


def main():
    radiopi = RadioPi()
    radiopi.main_loop()

if __name__ == '__main__':
    main()
