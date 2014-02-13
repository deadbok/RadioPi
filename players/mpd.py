'''
Generic mpd encapsulation

@since 12/02/2014
@author: oblivion
'''
import log
from urllib.parse import urlparse
from mpd import MPDClient
import sys


def connect(host):
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
