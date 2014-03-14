'''
Generic mpd encapsulation

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
