'''
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
