'''
Main file for RadioPi, an interface between various programs and an LCD, to
function as a sort of portable radio/media player.

@since 09/02/2014
@author: oblivion
'''
import optparse
from urllib.parse import urlparse
from lcdprocc.client import Client
from mpd import MPDClient
import log
import logging
from players import MpdMusic
from ui import screens
import sys

VERSION = '0.1'


def connect_lcdd(host='localhost'):
    '''
    Connect to LCDd.
    '''
    log.logger.info("Connecting to LCDd on " + host)
    # Parse the host address
    url = urlparse('//' + host)

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
        lcd = Client(hostname, port)
        lcd.request('client_set', '-name RadioPi')
        log.logger.debug('Connection succeeded')
        # Put the hook in place
        lcd.response_hook = lcd_hook
    except OSError as exception:
        log.logger.info('Can not connect to LCDd on ' + host)
        log.logger.debug('Exception: ' + str(exception.errno))
        log.logger.debug('Message: ' + exception.strerror)
        sys.exit(1)
    # Hangs because LCDd returns nothing on my machine
    # log.logger.debug(lcd.request('info'))
    return(lcd)


def connect_mpd(host='localhost'):
    '''
    Connect to mpd.
    '''
    log.logger.info("Connecting to mpd on " + host)
    # Parse the host address
    url = urlparse('//' + host)

    hostname = url.hostname
    port = url.port

    # Default to localhost port 6600
    if hostname == None:
        hostname = 'localhost'
    if port == None:
        port = 6600

    log.logger.debug('Hostname: ' + hostname)
    log.logger.debug('Port: ' + str(port))

    try:
        mpdc = MPDClient()
        mpdc.connect(hostname, port)
        log.logger.debug('Connection succeeded')
        log.logger.debug('MPD status: ' + str(mpdc.status()))
    except OSError as exception:
        log.logger.info('Can not connect to mpdd on ' + host)
        log.logger.debug('Exception: ' + str(exception.errno))
        log.logger.debug('Message: ' + exception.strerror)
        sys.exit(1)

    return(mpdc)


def lcd_hook(response):
    log.logger.debug("Response: " + response)
    if not response == None:
        print(response)


def main():
    '''
    Main entry point for RadioPi.
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

    # Connect to LCDd
    if len(args) > 0:
        lcd = connect_lcdd(args[0])
    else:
        lcd = connect_lcdd()

    # Connect to mpd
    if len(args) > 1:
        mpdc = connect_mpd(args[1])
    else:
        mpdc = connect_mpd()

    # Initialise players
    play_music = MpdMusic.MpdMusic(mpdc)

    scr_lcd = screens.Screens(lcd)

    scr_lcd.status.lines[1] = "bla"
    scr_lcd.status.lines[2] = "bla bla"
    scr_lcd.status.lines[3] = "bla bla bla"

    # Root menu
    lcd.request('menu_add_item', '"" radio menu "Radio"')
    lcd.request('menu_add_item', '"" music menu "Music"')
    lcd.request('menu_add_item', '"" settings menu "Settings"')

    while(1):
        scr_lcd.status.update()
        lcd.poll()
        print('.', end='')

if __name__ == '__main__':
    main()
