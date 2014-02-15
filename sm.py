'''
State machine for the main loop.

@since 15/02/2014
@author: oblivion
'''
import log
from collections import deque


class StateMachine(object):
    '''
    Simple state machine.
    '''
    states = dict()
    '''A dict of all states, the keys are the names, the values the function.'''
    state_queue = deque()
    '''Queue of states that needs to be run.'''
    default_state = ''
    '''Default state to run when there id no queued states.'''
    def __init__(self):
        '''
        Constructor
        '''
        log.logger.debug('Creating state machine')

    def create_state(self, name, func):
        '''
        Add a state.
        '''
        log.logger.debug('Adding state: ' + name)
        log.logger.debug('Function: ' + str(func))
        self.states[name] = func

    def next_state(self):
        '''
        Run the next state.
        '''
        if len(self.state_queue) == 0:
            name = self.default_state
        else:
            name = self.state_queue.popleft()
            log.logger.debug('Running state: ' + name)
        self.states[name]()

    def queue_state(self, name):
        '''
        Add a state to the queue.
        '''
        log.logger.debug('Adding state to queue: ' + name)
        self.state_queue.append(name)

    def set_default(self, name):
        '''
        Set the default state.
        '''
        log.logger.debug('Setting default state: ' + name)
        self.default_state = name
