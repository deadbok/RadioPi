'''
Created on 10/02/2014

@author: oblivion
'''
import log
from players.player import Player


class MpdMusic(Player):
    '''
    Class to use mpd to play music files.
    '''
    mpd = None
    '''MPDClient instance.'''

    def __init__(self, mpd):
        '''
        Constructor

        @param mpd: MPD Python client.
        @type mpd: mpd.MPDClient
        '''
        log.logger.debug("Creating mpd music player")
        Player.__init__(self, "Music")
        self.mpd = mpd
        # TODO: Remove this and make a menu entry or make it dynamic
        # Update database
        self.mpd.update()

    def get_items(self, uri):
        items = self.mpd.listall()
        filelist = list()
        for item in items:
            if 'file' in item:
                filelist.append(item['file'])
        return(filelist)
