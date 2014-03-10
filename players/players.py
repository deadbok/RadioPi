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
    '''Dictionary of all players, the keys are their name.'''
    mpd = None
    '''An instance of python-mpd2, as it is used by more than one player.'''

    def __init__(self, mpdhost):
        '''
        Constructor. "mpdhost" is the host and port of the mpd daemon.
        '''
        log.logger.debug("Initialising players")
        # Initialise mpd
        self.mpd = players.mpd.connect(mpdhost)
        # Initialise music player
        self.players['Music'] = MpdMusic(self.mpd)

    def close(self):
        '''
        This is the place to do cleanup when the app closes.
        '''
        if not self.mpd == None:
            self.mpd.close()
            self.mpd.disconnect()
