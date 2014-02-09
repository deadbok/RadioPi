'''
Main file for RadioPi, an interface between various programs and an LCD, to
function as a sort of portable radio/media player.

@since 09/02/2014
@author: oblivion
'''
import optparse
from urllib.parse import urlparse
from lcdproc.server import Server
from mpd import MPDClient
import log
import logging


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
        lcd = Server()
    except Exception as exception:
        log.logger.info('Can not connect to LCDd on ' + host)
        log.logger.debug('Exception: ' + str(exception.errno))
        log.logger.debug('Message: ' + exception.strerror)
    log.logger.debug('Connection succeeded')

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
    except Exception as exception:
        log.logger.info('Can not connect to mpdd on ' + host)
        log.logger.debug('Exception: ' + str(exception.errno))
        log.logger.debug('Message: ' + exception.strerror)
    log.logger.debug('Connection succeeded')
    log.logger.debug('MPD status: ' + str(mpdc.status()))

    return(mpdc)


def main():
    '''
    Main entry point for RadioPi.
    '''
    # mpd hostname or ip
    mpd_host = "localhost"

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

    # Save the hosts
    if len(args) > 1:
        mpd_host = args[1]

    log.logger.info("RadioPi V" + VERSION)

    # Connect to LCDd
    if len(args) > 0:
        lcd = connect_lcdd(args[0])
    else:
        lcd = connect_lcdd()

    # Connect to mpd
    if len(args) > 0:
        mpdc = connect_mpd(args[0])
    else:
        mpdc = connect_mpd()


if __name__ == '__main__':
    main()
