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
        # Remove the song from the playlist when done
        self.mpd.consume(1)
        # Clear the playlist
        self.mpd.clear()

    def get_items(self, uri):
        items = self.mpd.listall()
        filelist = list()
        for item in items:
            if 'file' in item:
                filelist.append(item['file'])
        return(filelist)

    def add_item(self, uri):
        '''
        Add an item to the playlist.
        '''
        log.logger.debug("Adding: " + uri)
        self.mpd.add(uri)

    def play(self):
        '''
        Play the current playlist.
        '''
        log.logger.debug("Playing...")
        self.playing = True
        self.mpd.play(0)

    def get_playing(self):
        '''
        Get the currently playing song.
        '''
        info = self.mpd.currentsong()
        if 'id' in info.keys():
            song = self.mpd.playlistid(info['id'])
            return(song[0]['title'])
        else:
            return('')
