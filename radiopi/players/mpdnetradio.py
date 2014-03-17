'''
This is the "Net Radio" player, it uses MPD to select stations from playlists.

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
from radiopi.log import logger
from radiopi.players.player import Player
from radiopi.ui.menuitem import MenuItem


STATION_LIST_PATH = 'netradio'
'''The folder in the library, where the station lists are at.'''


class MpdNetRadio(Player):
    '''
    Class to use mpd to select music files.
    '''
    mpd = None
    '''MPDClient instance.'''
    paused = False
    '''Tell if we are paused.'''

    def __init__(self, mpd):
        '''
        Constructor.
        '''
        logger.debug("Creating mpd net radio player")
        Player.__init__(self, "Net Radio")
        self.mpd = mpd
        # TODO: Remove this and make a menu entry or make it dynamic
        # Update database
        self.mpd.update()
        # Remove the song from the playlist when done
        self.mpd.consume(1)
        # Clear the playlist
        self.mpd.stop()
        self.mpd.clear()

    def get_stations(self, root, value):
        '''Create a lists stations in a list.'''
        logger.debug('Station menu.')
        if 'playlist' in value:
            items = self.mpd.listplaylistinfo(value['playlist'])
            menu = list()
            for item in items:
                if not item == '':
                    menu_item = MenuItem(item, item['name'], root=root)
                    menu.append(menu_item)
        return(menu)

    def get_station_lists(self, root):
        '''Create a list station lists.'''
        logger.debug('Station lists')
        items = self.mpd.lsinfo(STATION_LIST_PATH)
        menu = list()
        for item in items:
            if 'playlist' in item:
                name = item['playlist'].replace('netradio/', '').replace('.m3u', '')
                menu_item = MenuItem(item, name, True, root=root)
                menu.append(menu_item)
        return(menu)

    def get_menu(self, value, root):
        '''
        Return a list of menu items. Value determines the type of menu.
        '''
        menu = list()
        if isinstance(value, dict):
            menu = self.get_stations(root, value)
        else:
            # Empty is a special case, e.g. the browse type selection.
            if value == '':
                # Play/pause
                menu.append(MenuItem('pause', 'Play/Pause', root=root))
                # Albums
                menu.append(MenuItem('station lists', 'Station lists', True,
                                     root=root))
            else:
                if value == 'station lists':
                    menu = self.get_station_lists(root)
        return(menu)

    def add_item(self, value):
        '''
        Add a list of items to the playlist.
        '''
        logger.debug("Adding: " + str(value))
        self.mpd.add(value['file'])

    def select(self, value):
        '''
        Something has been selected. If the value is a list, play it, else it
        is a string of the menu item selected.
        '''
        logger.debug("Select: " + str(value))
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
            if value == 'pause':
                self.pause()

    def stop(self):
        '''
        Stop playing.
        '''
        logger.debug("Stop.")
        self.mpd.stop()

    def play(self, position=0):
        '''
        Play.
        '''
        logger.debug("Play.")
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
            logger.debug("Resume.")
        else:
            # Find out if something is playing (updates self.playing)
            self.get_playing()
            # If something is playing
            if self.playing:
                logger.debug("Pause.")
                self.mpd.pause()
                self.paused = True

    def get_playing(self):
        '''
        Get the currently playing song.
        '''
        info = self.mpd.currentsong()
        if 'name' in info.keys():
            self.playing = True
            return(info['name'])
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
