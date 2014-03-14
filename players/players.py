'''
Class to initialise and interface to all players.

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
