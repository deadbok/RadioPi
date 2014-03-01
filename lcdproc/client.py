'''
Simple client to talk to LCDd. It only understands command responses, and
passes everything else on to an external function using a queue.
'''
import telnetlib
from urllib.parse import unquote
from select import select
from collections import deque
import log


class LCDprocError(Exception):
    '''
    Generic exception.
    '''
    pass


class CommandError(LCDprocError):
    '''
    LCDd has returned an error after running a command.
    '''
    pass


class ProtocolError(LCDprocError):
    '''
    The client has received an unexpected response
    '''
    pass


class Client(object):
    '''
    LCDproc client
    '''
    response_hook = None
    '''Hook to handle responses from LCDd, "huh" and "success" are filtered
    out. Set this to a function that expects the response as a parameter.'''
    hook_busy = False
    '''Set if hook can not accept input.'''
    response_queue = deque()
    '''Queued responses.'''
    def __init__(self, hostname="localhost", port=13666):
        '''
        Constructor.
        '''
        self.hostname = hostname
        self.port = port
        self.server = telnetlib.Telnet(self.hostname, self.port)
        self.server_info = dict()

        # Send hello for session start
        response = self._request_nopoll('hello', '')
        # Split the return info and save data
        bits = response.split(" ")
        self.server_info.update({
            "server_version": bits[2],
            "protocol_version": bits[4],
            "screen_width": int(bits[7]),
            "screen_height": int(bits[9]),
            "cell_width": int(bits[11]),
            "cell_height": int(bits[13])
        })

    def _request_nopoll(self, command, param):
        '''
        Send a request to LCDd, and return the response. This is a special case
        function only used for the initial chat with LCDd
        '''
        log.logger.debug("Request: " + command + ' ' + param)
        self.server.write((command + ' ' + param + "\n").encode())

        response = unquote(self.server.read_until(b"\n").decode())
        log.logger.debug("Response: " + response)

        return(response)

    def request(self, command, param):
        '''
        Send a request to LCDd and wait for a response.
        '''
        # Send the commend
        log.logger.debug("Request: " + command + ' ' + param)
        self.server.write((command + ' ' + param + "\n").encode())
        # Wait for return status
        response = self.poll(True)
        # wait for an acceptable answer
        while response == None:
            response = self.poll(True)
        # Handle error
        if 'success' not in response:
            if 'huh' in response:
                raise CommandError('LCDproc returned: ' + response)
            else:
                raise ProtocolError('LCDproc returned: ' + response)

    def check_response(self, response):
        '''
        Check if the response is something we should deal with, e.g huh? and
        success.
        '''
        if not response == None:
            if "success" in response:
                return(True)
            elif "huh" in response:
                return(True)

        return(False)

    def poll(self, request=False):
        '''
        Get the status from LCDd. If the answer is unknown insert it in a
        queue, for the response hook to process. If a response to a command is
        not expected (request = False) pop items from the response hook queue,
        and serve them to the hook.
        '''
        # Pass on queued responses if the hook is ready
        if not request:
            if (len(self.response_queue) > 0) and not (self.hook_busy):
                log.logger.debug("Serving from queue.")
                self.response_hook(self.response_queue.popleft())
        # Check if server is ready for reading
        while select([self.server], [], [], 0) == ([self.server], [], []):
            response = unquote(self.server.read_until(b"\n").decode())
            log.logger.debug("Response: " + response)
            # Do we understand the response
            if self.check_response(response):
                if request:
                    log.logger.debug('Leaving poll: ' + response)
                    return response
                else:
                    raise ProtocolError('Unexpected response: ' + response)
            # Send the response on to the hook
            else:
                if not self.response_hook == None:
                    log.logger.debug('Adding to queue: ' + response)
                    self.response_queue.append(response)
        return(None)

    def close(self):
        '''Close the connection.'''
        self.server.close()
