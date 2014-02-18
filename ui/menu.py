'''

@since 11/02/2014
@author: oblivion
'''
import log
from uuid import uuid4
from ui.menuitem import MenuItem


class Menu(object):
    '''
    All menu stuff
    '''
    lcd = None
    '''Connection to LCDd'''
    menu = dict()
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
        log.logger.debug("Initialising menus")
        self.lcd = lcd

    def set_root_menu(self, menu):
        '''
        There can be only one. Only display our menu.
        '''
        self.lcd.request('menu_set_main', '"' + menu + '"')

    def enter(self, menu, items):
        '''
        A menu has been selected.
        '''
        self.generate_menu(menu, items)

    def leave(self, menu):
        '''
        A menu has been left.
        '''
        self.last_menu_name = menu

    def generate_back_item(self, menu):
        '''
        Generate a back navigation item.
        '''
        # Delete old back button
        if 'dback' in self.menu:
            self.lcd.request('menu_del_item', '"' + menu
                                 + '" "dback"')
        item = MenuItem('dback', '< Back', False, 'dback')
        # Set root
        item.root = menu
        self.menu[item.id] = item
        self.lcd.request('menu_add_item', '"' + menu + '" "' + str(item.id)
                             + '" action "' + item.text + '"')
#         self.lcd.request('menu_set_item', '"' + path
#                          + '" dback -next "' + self.last_menu_name + '"')

    def generate_menu(self, path, items):
        '''
        Generate a menu.
        '''

        log.logger.debug('Generating list menu: ' + path)
        # Check if its there already
#         if path in self.menu.keys():
#             log.logger.debug('Menu has already been generated')
#             return()

        # Create the menu
        for item in items:
            log.logger.debug('Menu item: ' + str(item.id))
            log.logger.debug('Menu item text: ' + item.text)
            # Set root
            item.root = path
            # Save the entry
            self.menu[item.id] = item
            if not item.submenu:
                # Create an item that closes the menu when selected
                self.lcd.request('menu_add_item', '"' + path + '" "' + str(item.id)
                             + '" action "' + item.text + '"')
                self.lcd.request('menu_set_item', '"' + path + '" "' + str(item.id)
                                 + '" -next _quit_')
            else:
                # Create the an item that closes the menu when selected
                self.lcd.request('menu_add_item', '"' + path + '" "' + str(item.id)
                             + '" menu "' + item.text + '"')
        self.generate_back_item(path)

    def delete_menu(self):
        '''
        Delete a menu.
        '''
        log.logger.debug('Deleting menu')
        # Move the back button to the root menu
        if not self.menu['dback'].root == '':
            self.generate_back_item()
        for item in self.menu.values():
            # Don't delete the back button
            if not item.value == 'dback':
                self.lcd.request('menu_del_item', '"' + item.root
                                 + '" "' + str(item.id) + '"')
