'''
State machine for the main loop.

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
from collections import deque


class MissingStateError(Exception):
    '''
    Exception when trying to run a missing state.
    '''
    pass


class StateMachine(object):
    '''
    Simple state machine.
    '''
    states = dict()
    '''A dict of all states, the keys are the names, the values the function'''
    state_queue = deque()
    '''Queue of states that needs to be run.'''
    default_state = ''
    '''Default state to run when there id no queued states.'''
    def __init__(self):
        '''
        Constructor
        '''
        logger.debug('Creating state machine')

    def create_state(self, name, func):
        '''
        Add a state.
        '''
        logger.debug('Adding state: ' + name)
        logger.debug('Function: ' + str(func))
        self.states[name] = func

    def next_state(self):
        '''
        Run the next state.
        '''
        if len(self.state_queue) == 0:
            name = self.default_state
        else:
            name = self.state_queue.popleft()
            logger.debug('Running state: ' + name)
        # Run state if it exists
        if name in self.states.keys():
            self.states[name]()
        else:
            raise MissingStateError('State machine missing state: ' + name)

    def queue_state(self, name):
        '''
        Add a state to the queue.
        '''
        logger.debug('Adding state to queue: ' + name)
        self.state_queue.append(name)

    def set_default(self, name):
        '''
        Set the default state.
        '''
        logger.debug('Setting default state: ' + name)
        self.default_state = name
