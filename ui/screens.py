'''
Created on 10/02/2014

@author: oblivion
'''
from .status import Status
import log


class Screens(object):
    '''
    Class holding the static LCD screens.
    '''
    status = None
    '''Status screen (default screen)'''

    def __init__(self, lcd):
        '''
        Constructor.

        @param lcd: The interface to LCDd.
        @type lcd: lcdproc.server.Server
        '''
        log.logger.debug('Creating screens.')
        self.status = Status(lcd)
