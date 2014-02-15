'''

@since 11/02/2014
@author: oblivion
'''
import log


class Menu(object):
    '''
    All menu stuff
    '''
    lcd = None
    '''Connection to LCDd'''
    dynamic_menu = dict()
    '''Dictionary of items in the current dynamic menu'''
    dynamic_menu_name = ''
    '''Name of the current dynamic menu'''
    last_menu_name = '""'
    '''Name of the previous menu'''
    def __init__(self, lcd, players):
        '''
        Constructor

        @param lcd: LCDd python client.
        @type lcd: lcdproc.client.Client
        @param players: Dictionary of players and menu names
        @type players: dict
        '''
        log.logger.debug("Initialising menus")
        self.lcd = lcd
        # Root menu player entries
        for name in players.keys():
            self.lcd.request('menu_add_item', '"" ' + name + ' menu "' + name
                             + '"')
        # Root Settings menu
        self.lcd.request('menu_add_item', '"" Settings menu "Settings"')
        # Get out of the menu
        self.lcd.request('menu_add_item', '"" back action "< Back"')
        self.lcd.request('menu_set_item', '"" back -next _quit_')

        # There can be only one. Only display our menu
        self.lcd.request('menu_set_main', '""')

    def generate_selection_list(self, menu, items):
        '''
        Generate a list menu, meant for listing files or playlists.
        '''
        log.logger.debug('Generating list menu: ' + menu)
        # Delete old back button
        if not self.dynamic_menu_name == '':
            self.lcd.request('menu_del_item', '"' + self.dynamic_menu_name
                             + '" dback')
        # Create the menu
        self.dynamic_menu_name = menu
        self.dynamic_menu = items
        for item in items.items():
            if 'action' in item[1][0]:
                # Create the an item that closes the menu when selected
                self.lcd.request('menu_add_item', '"' + menu + '" "' + item[0]
                             + '" action "' + item[0] + '"')
                self.lcd.request('menu_set_item', '"' + menu + '" "' + item[0]
                                 + '" -next _quit_')
            elif 'menu' in item[1][0]:
                # Create the an item that closes the meu when selected
                self.lcd.request('menu_add_item', '"' + menu + '" "' + item[0]
                             + '" menu "' + item[0] + '"')
        self.lcd.request('menu_add_item', '"' + menu
                         + '" dback action "< Back"')
        self.lcd.request('menu_set_item', '"' + menu
                         + '" dback -next "' + self.last_menu_name + '"')

    def delete_selection_list(self, menu=''):
        '''
        Delete a list menu.
        '''
        # Clear the menu if it's the right one.
        # If '' an empty string is given the menu is cleared
        if (menu == self.dynamic_menu_name) or (menu == ''):
            log.logger.debug('Deleting list menu: ' + menu)
            for item in self.dynamic_menu:
                self.lcd.request('menu_del_item', '"' + self.dynamic_menu_name
                                 + '" "' + item + '"')
            self.lcd.request('menu_del_item', '"' + self.dynamic_menu_name
                             + '" dback')

    def enter(self, menu, items):
        '''
        A sub menu has been selected.
        '''
        self.generate_selection_list(menu, items)

    def leave(self, menu):
        '''
        A sub menu has been left.
        '''
        self.last_menu_name = menu
