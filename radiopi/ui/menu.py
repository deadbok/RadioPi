'''
This deals with menu functions. It keeps an internal representation of the
menu, as well as the one send to LCDd. The menus a generated on the fly, when
first accessed.

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
from collections import OrderedDict
from radiopi.ui.menuitem import MenuItem


class Menu(object):
    '''
    All menu stuff
    '''
    lcd = None
    '''Connection to LCDd'''
    menu = OrderedDict()
    '''Dictionary of items in the menu'''
    dynamic_menu_name = ''
    '''Name of the current dynamic menu'''
    last_menu_name = '""'
    '''Name of the previous menu'''
    menu_path = '/'
    '''The current items that has been selected to get at the current menu.'''
    def __init__(self, lcd):
        '''
        Constructor

        @param lcd: LCDd python client.
        @type lcd: lcdproc.client.Client
        @param players: Dictionary of players and menu names
        @type players: dict
        '''
        logger.debug("Initialising menus")
        self.lcd = lcd

    def set_root(self, menu):
        '''
        There can be only one. Only display our menu.
        '''
        self.lcd.request('menu_set_main', '"' + menu + '"')

    def generate_back_item(self, menu=''):
        '''
        Generate a back navigation item.
        '''
        logger.debug('Auto generating back button')
        # Delete old back button
        if 'dback' in self.menu:
            self.lcd.request('menu_del_item', '"' + menu
                                 + '" "dback"')
        item = MenuItem('dback', '< Back', False, 'dback', root=menu)
        self.menu[item._id] = item
        self.lcd.request('menu_add_item', '"' + menu + '" "' + item._id
                             + '" action "' + item.text + '"')
        self.lcd.request('menu_set_item', '"' + menu
                         + '" dback -menu_result close')
        return(item)

    def generate(self, root, items):
        '''
        Generate a menu.

        @param root: The menu item that the menu belongs to.
        @param items: A list of items the create in the menu.
        '''
        logger.debug('Generating menu')
        # Create the menu
        for item in items:
            logger.debug('Menu item: ' + item._id)
            logger.debug('Menu item text: ' + item.text)
            # If the item has not been send already
            if item._id not in self.menu.keys():
                # Send to LCDd
                item.send(self.lcd)
                # Save the entry
                self.menu[item._id] = item

            else:
                logger.debug('Menu item has already been generated')
        # Create back button
        self.generate_back_item(root)

    def delete(self):
        '''
        Delete a menu.
        '''
        logger.debug('Deleting menu')
        # Delete back button first to save us some trouble.
        # LCDd expect sub-menus to be deleted before menus. I haven't looked
        # into what happens other than you can't delete a menu item, when the
        # menu has been deleted. That is why I use an OrderedDict. The dynamic
        # back button is changed with every menu change, and can't be expected
        # to be at the right place in the dict
        if 'dback' in self.menu:
            item = self.menu['dback']
            self.lcd.request('menu_del_item', '"' + item.root + '" "dback"')
            del self.menu['dback']
        while len(self.menu) > 0:
            _, item = self.menu.popitem(True)
            # LCDd removes a menu when it is empty, so skip them
            if not item.submenu:
                logger.debug('Menu     item: ' + item._id)
                logger.debug('Menu item text: ' + item.text)
                self.lcd.request('menu_del_item', '"' + item.root
                                     + '" "' + item._id + '"')

    def goto(self, _id):
        '''
        Activate a specific menu.
        '''
        self.lcd.request('menu_goto', '"' + _id + '"')
