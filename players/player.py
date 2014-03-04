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

    def get_menu(self, value, root):
        '''
        Return a list of all playable items, wrapped in MenuItems.
        '''
        raise NotImplementedError('Must be implemented in a derived class')

    def add_item(self, value):
        '''
        Add an item to the current playlist.
        '''
        raise NotImplementedError('Must be implemented in a derived class')

    def select(self, value):
        '''
        Start playing.
        '''
        raise NotImplementedError('Must be implemented in a derived class')

    def stop(self):
        '''
        Stop playing.
        '''
        raise NotImplementedError('Must be implemented in a derived class')

    def play(self):
        '''
        Play.
        '''
        raise NotImplementedError('Must be implemented in a derived class')

    def pause(self):
        '''
        Pause/unpause playing.
        '''
        raise NotImplementedError('Must be implemented in a derived class')

    def get_playing(self):
        '''
        Get the currently playing song.
        '''
        raise NotImplementedError('Must be implemented in a derived class')

    def up(self):
        '''
        React when the 'Up' button is pressed.
        '''
        raise NotImplementedError('Must be implemented in a derived class')

    def down(self):
        '''
        React when the 'Down' button is pressed.
        '''
        raise NotImplementedError('Must be implemented in a derived class')
