'''
MenuItem holds a menu item!!!!! Wow.

@since 17/02/2014
@author: oblivion
'''
from uuid import uuid4


class MenuItem(object):
    '''
    Class for an item in the menu.
    '''
    id = ''
    '''The id assigned to the menu entry.'''
    text = ''
    '''The visible text of the menu item.'''
    value = ''
    '''The value, usually the path to the file that has been selected.'''
    submenu = True
    '''Does this item have a submenu.'''
    root = ''
    '''Name of the root menu for this item.'''
    def __init__(self, value, text, submenu=False, id=''):
        '''
        Constructor.
        '''
        self.text = text
        self.value = value
        self.submenu = submenu
        if id == '':
            self.create_id()
        else:
            self.id = id

    def create_id(self):
        '''
        Create a unique id.
        '''
        self.id = str(hash(self))
        return(self.id)
