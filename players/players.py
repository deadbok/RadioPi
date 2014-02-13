'''
Class to initialise and interface to all players.

@since 12/02/2014
@author: oblivion
'''
import log
import players.mpd
from players.mpdmusic import MpdMusic


class Players(object):
    '''
    Interface to all players
    '''
    players = dict()

    def __init__(self, mpdhost):
        '''
        Constructor

        @param mpdhost: The host and port of the mpd daemon.
        @type mpdhost: string
        '''
        log.logger.debug("Initialising players")
        # Initialise mpd
        mpd = players.mpd.connect(mpdhost)
        # Initialise music player
        self.players['Music'] = MpdMusic(mpd)
