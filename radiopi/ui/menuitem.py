'''
MenuItem holds a menu item!!!!! Wow.

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


class MenuItem(object):
    '''
    Class for an item in the menu.
    '''
    _id = ''
    '''The id assigned to the menu entry.'''
    text = ''
    '''The visible text of the menu item.'''
    value = ''
    '''The value. Data used by the player.'''
    submenu = True
    '''Does this item have a submenu.'''
    root = ''
    '''Name of the root menu for this item.'''
    def __init__(self, value, text, submenu=False, _id='', root=''):
        '''
        Constructor.
        '''
        logger.debug('Creating menu item: ' + text)
        logger.debug('Menu item root: ' + root)
        self.text = text
        self.value = value
        self.submenu = submenu
        self.root = root
        if _id == '':
            self.create_id()
        else:
            self._id = _id

    def create_id(self):
        '''
        Create a id from text and root item.
        '''
        self._id = str(hash(self.text + self.root))
        logger.debug('Creating menu id: ' + self._id)
        return(self._id)

    def send(self, lcd):
        '''Send the button to LCDd.'''
        logger.debug('Sending button: ' + self._id)
        if not self.submenu:
            # Create an item that closes the menu when selected
            lcd.request('menu_add_item', '"' + self.root + '" "'
                             + self._id + '" action "' + self.text
                             + '"')
            lcd.request('menu_set_item', '"' + self.root + '" "'
                             + self._id + '" -next _quit_')
        else:
            # Create a menu with sub items
            lcd.request('menu_add_item', '"' + self.root + '" "'
                             + self._id + '" menu "' + self.text + '"')
