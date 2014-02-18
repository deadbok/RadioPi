'''
Created on 10/02/2014

@author: oblivion
'''


class Player(object):
    '''
    Base class for all audio players.
    '''
    name = ""
    '''Name of the player in the menu.'''
    status = ('', '', '')
    '''3 lines of status text.'''
    playing = False
    '''Is the player playing.'''
    def __init__(self, name):
        '''
        Constructor.

        @param name: The name of the player to display in the menu.
        @type name: String
        '''
        self.name = name

    def get_items(self, uri):
        '''
        Return a list of all playable items, wrapped in MenuItems.
        '''
        raise NotImplementedError('Must be implemented in a derived class')

    def add_item(self, uri):
        '''
        Add an item to the current playlist.
        '''
        raise NotImplementedError('Must be implemented in a derived class')

    def play(self):
        '''
        Start playing.
        '''
        raise NotImplementedError('Must be implemented in a derived class')

    def stop(self):
        '''
        Stop playing.
        '''
        raise NotImplementedError('Must be implemented in a derived class')

    def get_playing(self):
        '''
        Get the currently playing song.
        '''
        raise NotImplementedError('Must be implemented in a derived class')

    def menu_items(self):
        '''
        Generate menu items for control of the player.
        '''
        raise NotImplementedError('Must be implemented in a derived class')
