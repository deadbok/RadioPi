'''
Main file for RadioPi, an interface between various programs and an LCD, to
function as a sort of portable radio/media player.

@since 09/02/2014
@author: oblivion
'''
import optparse
from lcdproc.server import Server
from mpd import MPDClient
import log
import logging

VERSION = '0.1'


def main():
    '''
    Main entry point for RadioPi.
    '''
    # lcdproc hostname or ip
    lcd_host = "localhost"
    # mpd hostname or ip
    mpd_host = "localhost"

    usage = "usage: %prog [options] lcd_host mpd_host"
    arg_parser = optparse.OptionParser(usage=usage)
    arg_parser.add_option("-v", "--verbose",
                          action="store_true", dest="verbose",
                          default=False,
                          help="Print detailed progress [default]")
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
    else:
        log.init_console_log()

    # Save the hosts
    if len(args) > 0:
        lcd_host = args[0]
    if len(args) > 1:
        mpd_host = args[1]

    log.logger.info("RadioPi V" + VERSION)

    # Connect to LCDd
    log.logger.debug("Connecting to LCDd on " + lcd_host)
    try:
        lcd = Server()
    except Exception as exception:
        log.logger.info('Can not connect to LCDd on ' + lcd_host)
        log.logger.debug('Exception: ' + str(exception.errno))
        log.logger.debug('Message: ' + exception.strerror)
    log.logger.debug('Connection succeeded')

    log.logger.info('Connecting to MPD on ' + mpd_host)
    try:
        mpdc = MPDClient()
        mpdc.connect(mpd_host, 6600)
    except Exception as exception:
        log.logger.info('Can not connect to LCDd on ' + lcd_host)
        log.logger.debug('Exception: ' + str(exception.errno))
        log.logger.debug('Message: ' + exception.strerror)
    log.logger.debug('Connection succeeded')
    log.logger.debug('MPD status: ' + str(mpdc.status()))

if __name__ == '__main__':
    main()
