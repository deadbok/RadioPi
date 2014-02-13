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

    def generate_selection_list(self, menu, lst):
        '''
        Generate a list menu, meant for listing files or playlists.
        '''
        log.logger.debug('Generating list menu')
        i = 0
        for item in lst:
            self.lcd.request('menu_add_item', '"' + menu + '" ' + str(i)
                         + ' action "' + item + '"')
            self.lcd.request('menu_set_item', '"' + menu + '" ' + str(i)
                             + ' -next _quit_')
            i += 1
        self.lcd.request('menu_add_item', '"' + menu
                         + '" dback action "< Back"')

    def delete_selection_list(self, menu, lst):
        '''
        Delete a list menu.
        '''
        log.logger.debug('Deleting list menu')
        i = 0
        for item in lst:
            self.lcd.request('menu_del_item', '"' + menu + '" ' + str(i))
            i += 1
        self.lcd.request('menu_del_item', '"' + menu + '" dback')
