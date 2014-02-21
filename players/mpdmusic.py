'''
This is the "Music" player, it uses MPD to play music from the filesystem.
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
    Class to use mpd to play music files.
    '''
    mpd = None
    '''MPDClient instance.'''

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
        Create a list of files and dirctories in the current value, wrapped in
        MenuItem classes.
        '''
        items = self.mpd.lsinfo(value.directory)
        menu = list()
        for item in items:
            if 'file' in item:
                item_value = ItemValue(value.directory, item['file'], 'Files')
                menu_item = MenuItem(item_value, basename(item['file']))
                menu_item.root = root
                # Hash the ID after the root has been added
                menu_item.create_id()
                menu.append(menu_item)
            elif 'directory' in item:
                item_value = ItemValue(item['directory'], '', 'Files')
                menu_item = MenuItem(item_value,
                                     relpath(item['directory'], value.directory),
                                     True)
                menu_item.root = root
                # Hash the ID after the root has been added
                menu_item.create_id()
                menu.append(menu_item)
        return(menu)

    def get_by_artist(self, value, root):
        '''
        Create a list of at first level artists, then albums by artists, then
        songs.
        '''
        # Start by finding all artists
        if value.artist == '':
            items = self.mpd.list('artist')
            menu = list()
            # Sort them before running through them
            for item in sorted(items, key=cmp_to_key(locale.strcoll)):
                item = item.replace('Artist: ', '')
                if not item == '':
                    item_value = ItemValue(artist=item,
                                           browsetype='Artists')
                    menu_item = MenuItem(item_value, item, True)
                    menu_item.root = root
                    # Hash the ID after the root has been added
                    menu_item.create_id()
                    menu.append(menu_item)
            return(menu)
        # An artist has been selected
        else:
            # No album has been selected
            if value.album == '':
                items = self.mpd.search('artist', value.artist)
                albums = set()
                # Isolate albums
                for item in items:
                    albums.add(item['album'])
                menu = list()
                for album in albums:
                    if not album == '':
                        item_value = ItemValue(artist=item, album=album,
                                               browsetype='Artists')
                        menu_item = MenuItem(item_value, album, True)
                        menu_item.root = root
                        # Hash the ID after the root has been added
                        menu_item.create_id()
                        menu.append(menu_item)
                return(menu)


    def get_items(self, value, root):
        '''
        Return all items in value in a list og MenuItems. The first position in
        the value can be either Albums, Artists, or Files, and generates a list
        of the given type.
        '''
        menu = list()
        # Empty is a special case
        if value == '':
            menu = list()
            # Albums
            menu_item = MenuItem(ItemValue(browsetype='Albums'), 'Albums',
                                 True)
            menu_item.root = root
            # Hash the ID after the root has been added
            menu_item.create_id()
            menu.append(menu_item)
            # Artists
            menu_item = MenuItem(ItemValue(browsetype='Artists'), 'Artists',
                                 True)
            menu_item.root = root
            # Hash the ID after the root has been added
            menu_item.create_id()
            menu.append(menu_item)
            # Files
            menu_item = MenuItem(ItemValue(browsetype='Files'), 'Files', True)
            menu_item.root = root
            # Hash the ID after the root has been added
            menu_item.create_id()
            menu.append(menu_item)
        if isinstance(value, ItemValue):
            # File browser
            if value.browsetype == 'Files':
                menu = self.get_files(value, root)
            # Artists browser
            if value.browsetype == 'Artists':
                menu = self.get_by_artist(value, root)
        return(menu)

    def add_item(self, value):
        '''
        Add an item to the playlist.
        '''
        log.logger.debug("Adding: " + value.filename)
        self.mpd.add(value.filename)

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
