'''
Created on 10/02/2014

@author: oblivion
'''
from players.Player import Player


class MpdMusic(Player):
    '''
    Class to use mpd to play music files.
    '''
    mpdc = None
    '''MPDClient instance.'''

    def __init__(self, mpdc):
        '''
        Constructor

        @param mpdc: MPD Python client.
        @type mpdc: mpd.MPDClient
        '''
        Player.__init__(self, "Music")
        self.mpdc = mpdc
