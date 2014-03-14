'''
This is the "Music" player, it uses MPD to select music from the filesystem.

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
import locale
from os.path import basename, relpath
from functools import cmp_to_key
from players.player import Player
from ui.menuitem import MenuItem


class ItemValue(object):
    '''
    Container for the values needed to keep track items.
    '''
    directory = ''
    '''The directory of the item.'''
    filename = ''
    '''The filename of the item.'''
    artist = ''
    '''The artist of the item.'''
    album = ''
    '''The album of the item.'''
    browsetype = 'Files'
    '''The way to browse this item. Artists, Albums or Files.'''
    def __init__(self, directory='', filename='', artist='', album='',
                 browsetype='Files'):
        self.directory = directory
        self.filename = filename
        self.artist = artist
        self.album = album
        self.browsetype = browsetype


class MpdMusic(Player):
    '''
    Class to use mpd to select music files.
    '''
    mpd = None
    '''MPDClient instance.'''
    browse_type = 0
    '''The way that music is browsed.'''
    BROWSE_NONE = 0
    '''No browsing.'''
    BROWSE_FILES = 1
    '''Browsing files.'''
    BROWSE_ARTIST = 2
    '''Browsing by artist.'''
    BROWSE_ALBUM = 3
    '''Browsing by album.'''
    BROWSE_TRACK = 4
    '''Browsing by track.'''
    paused = False
    '''Tell if we are paused.'''

    def __init__(self, mpd):
        '''
        Constructor.
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

    def get_files(self, value, root):
        '''
        Create a list of files and directories in the current value, wrapped in
        MenuItem classes.
        '''
        log.logger.debug('Selecting by filename.')
        # Value is an emtpy string if this is the top level
        if str(value) == '':
            items = self.mpd.lsinfo(value)
            directory = ''
        else:
            items = self.mpd.lsinfo(value['directory'])
            directory = value['directory']
        menu = list()
        for item in items:
            if 'file' in item:
                menu_item = MenuItem([item], basename(item['file']), root=root)
                menu.append(menu_item)
            elif 'directory' in item:
                menu_item = MenuItem(item,
                                     relpath(item['directory'],
                                             directory),
                                     True, root=root)
                menu.append(menu_item)
        return(menu)

    def get_by_artist(self, root):
        '''
        Create a list of artists.
        '''
        log.logger.debug('Selecting by artist')
        items = self.mpd.list('artist')
        menu = list()
        # Sort them before running through them
        for item in sorted(items, key=cmp_to_key(locale.strcoll)):
            item = item.replace('Artist: ', '')
            if not item == '':
                menu_item = MenuItem(item, item, True, root=root)
                menu.append(menu_item)
        # Go to album selection next.
        self.browse_type = self.BROWSE_ALBUM
        return(menu)

    def get_by_album(self, root, artist=''):
        '''Create a list of albums, a optionally only by 'artist'.'''
        log.logger.debug('Album selection. Artist: ' + artist)
        if artist == '':
            items = self.mpd.list('album')
        else:
            items = self.mpd.list('album', artist)
        menu = list()
        for item in items:
            item = item.replace('Album: ', '')
            if not item == '':
                menu_item = MenuItem(item, item, True, root=root)
                menu.append(menu_item)
        # Select by track next
        self.browse_type = self.BROWSE_TRACK
        return(menu)

    def get_by_track(self, root, album):
        '''Create a list of tracks on an album.'''
        log.logger.debug('Track selection. Album: ' + album)
        items = self.mpd.search('album', album)
        menu = list()
        # Create an entry that plays the whole album
        menu_item = MenuItem(items, 'All', root=root)
        menu.append(menu_item)
        for item in items:
            menu_item = MenuItem([item], item['title'], root=root)
            menu.append(menu_item)
        return(menu)

    def get_menu(self, value, root):
        '''
        Return a list of menu items. Value determines the type of menu.
        '''
        menu = list()
        # Empty is a special case, e.g. the browse type selection.
        if value == '':
            # Play/pause
            menu.append(MenuItem('pause', 'Play/Pause', root=root))
            # Clear playlist
            menu.append(MenuItem('clear', 'Clear', root=root))
            # Albums
            menu.append(MenuItem(self.BROWSE_ALBUM, 'Albums', True, root=root))
            # Artists
            menu.append(MenuItem(self.BROWSE_ARTIST, 'Artists', True,
                                 root=root))
            # Files
            menu.append(MenuItem(self.BROWSE_FILES, 'Files', True, root=root))
        else:
            # If browse_type is BROWSE_NONE, this is the top level after
            # browsing type has been selected.
            if self.browse_type == self.BROWSE_NONE:
                # Set the browse type from the value
                self.browse_type = value
                value = ''
            # Call the right browser
            if self.browse_type == self.BROWSE_FILES:
                menu = self.get_files(value, root)
            elif self.browse_type == self.BROWSE_ARTIST:
                menu = self.get_by_artist(root)
            elif self.browse_type == self.BROWSE_ALBUM:
                menu = self.get_by_album(root, value)
            elif self.browse_type == self.BROWSE_TRACK:
                menu = self.get_by_track(root, value)
        return(menu)

    def add_item(self, value):
        '''
        Add a list of items to the playlist.
        '''
        log.logger.debug("Adding: " + str(value))
        # Finished browsing
        self.browse_type = self.BROWSE_NONE
        for item in value:
            self.mpd.add(item['file'])

    def select(self, value):
        '''
        Something has been selected. If the value is a list, play it, else it
        is a string of the menu item selected.
        '''
        log.logger.debug("Select: " + str(value))
        # If value is not a string, it should be something we can play
        if not isinstance(value, str):
            # Add to playlist
            self.add_item(value)
            # Find out if something is playing (updates self.playing)
            self.get_playing()
            # Start playing if stopped
            if not self.playing:
                self.play()
        else:
            if value == 'clear':
                self.mpd.clear()
            elif value == 'pause':
                self.pause()

    def stop(self):
        '''
        Stop playing.
        '''
        log.logger.debug("Stop.")
        self.mpd.stop()

    def play(self, position=0):
        '''
        Play.
        '''
        log.logger.debug("Play.")
        self.mpd.play(position)

    def pause(self):
        '''
        Pause/unpause playing.
        '''
        # Check if we are paused.
        if self.paused:
            # Simple resume.
            self.mpd.pause()
            self.paused = False
            log.logger.debug("Resume.")
        else:
            # Find out if something is playing (updates self.playing)
            self.get_playing()
            # If something is playing
            if self.playing:
                log.logger.debug("Pause.")
                self.mpd.pause()
                self.paused = True

    def get_playing(self):
        '''
        Get the currently playing song.
        '''
        info = self.mpd.currentsong()
        if 'id' in info.keys():
            song = self.mpd.playlistid(info['id'])
            self.playing = True
            return(song[0]['title'])
        else:
            self.playing = False
            return('')

    def up(self):
        '''
        React when the 'Up' button is pressed.
        '''
        self.mpd.previous()

    def down(self):
        '''
        React when the 'Down' button is pressed.
        '''
        self.mpd.next()
