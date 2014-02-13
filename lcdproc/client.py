import telnetlib
from urllib.parse import unquote
from select import select
from collections import deque
import log


class LCDprocError(Exception):
    pass


class CommandError(LCDprocError):
    pass


class ProtocolError(LCDprocError):
    pass


class Client(object):
    '''
    LCDproc client
    '''
    response_hook = None
    '''Hook to handle responses from LCDd, "huh" and "success" are filtered out.
    Set this to a function that expects the response as a parameter.'''
    hook_busy = False
    '''
    Set if hook can not accept input.
    '''
    response_queue = deque()
    '''
    Queued responses.
    '''
    def __init__(self, hostname="localhost", port=13666):
        '''
        Constructor.

        @param hostname: The hostname of the LCDd.
        @type hostname: string
        @param port: Port of the LCDd.
        @type port: int
        '''
        self.hostname = hostname
        self.port = port
        self.server = telnetlib.Telnet(self.hostname, self.port)
        self.server_info = dict()

        # Send hello for session start
        response = self.request_nopoll('hello', '')
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

    def request_nopoll(self, command, param):
        '''
        Send a request to LCDd, and return the response.

        @param command: The command to send to LCDd.
        @type command: string
        @param param: The parameters to send with the command
        @type param: string
        @return: The response from LCDd
        '''
        log.logger.debug("Request: " + command + ' ' + param)
        self.server.write((command + ' ' + param + "\n").encode())

        response = unquote(self.server.read_until(b"\n").decode())
        log.logger.debug("Response: " + response)

        return(response)

    def request(self, command, param):
        '''
        Send a request to LCDd. Wait for a response, and send unknown responses
        to the hook.

        @param command: The command to send to LCDd.
        @type command: string
        @param param: The parameters to send with the command
        @type param: string
        '''
        # Send the commend
        log.logger.debug("Request: " + command + ' ' + param)
        self.server.write((command + ' ' + param + "\n").encode())
        # Wait for return status
        response = self.poll(True)
        # wait for an acceptable answer
        while not self.check_response(response):
            response = self.poll(True)
        # Handle error
        if 'success' not in response:
            if 'huh' in response:
                raise CommandError('LCDproc returned: ' + response)
            else:
                raise ProtocolError('LCDproc returned: ' + response)

    def check_response(self, response):
        '''
        Check if the response is something we should deal with.

        @param response: The response from LCDd
        @type response: string
        @return: True if we know the response else return False
        '''
        if not response == None:
            if "success" in response:
                return(True)
            elif "huh" in response:
                return(True)

        return(False)

    def poll(self, request=False):
        '''
        Get the status from LCDd. If the answer is unknown send it on to the
        hook.
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
                        return response
                else:
                    raise ProtocolError('Unexpected response: ' + response)
            # Send the response on to the hook
            else:
                if not self.response_hook == None:
                    # Queue responses if hook is busy or we are waiting for
                    # a response to a request
                    # if self.hook_busy or request:
                    log.logger.debug('Adding to queue: ' + response)
                    self.response_queue.append(response)
                    # else:
                        # self.response_hook(response)

        return(None)
