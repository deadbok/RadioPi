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

    def __init__(self, name):
        '''
        Constructor.

        @param name: The name of the player to display in the menu.
        @type name: String
        '''
        self.name = name

    def get_items(self, uri):
        '''
        Return a list of all playable items.
        '''
        return(None)
