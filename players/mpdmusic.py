'''
Created on 10/02/2014

@author: oblivion
'''
import log
from os.path import basename, relpath
from players.player import Player
from ui.menuitem import MenuItem


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

    def get_items(self, uri, root):
        '''
        Return all items in uri in a list og MenuItems.
        '''
        items = self.mpd.lsinfo(uri)
        menu = list()
        for item in items:
            if 'file' in item:
                value = (uri, item['file'])
                menu_item = MenuItem(value, basename(item['file']))
                menu_item.root = root
                menu_item.create_id()
                menu.append(menu_item)
            elif 'directory' in item:
                value = (item['directory'], '')
                menu_item = MenuItem(value, relpath(item['directory'], uri),
                                     True)
                menu_item.root = root
                menu_item.create_id()
                menu.append(menu_item)
        return(menu)

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

    def menu_items(self):
        '''
        Generate menu items for control of the player.
        '''
        items = list()
        items.append(MenuItem('Play/Pause'))
        items.append(MenuItem('Next'))
        items.append(MenuItem('Prev'))
        items.append(MenuItem('Clear'))

        return(items)
