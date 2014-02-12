import telnetlib
from urllib.parse import unquote
from select import select
import log


class Client(object):
    '''
    LCDproc client Object
    '''
    response_hook = None

    def __init__(self, hostname="localhost", port=13666):
        '''
        Constructor.

        @param hostname: The hostname of the LCDd.
        @type hostname: string
        @param port: Port of the LCDd.
        @type port: int
        @param logger: A logger instance to output debug information to
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
        '''
        log.logger.debug("Request: " + command + ' ' + param)
        self.server.write((command + ' ' + param + "\n").encode())

        response = unquote(self.server.read_until(b"\n").decode())
        log.logger.debug("Response: " + response)

        return(response)

    def request(self, command, param):
        '''
        Send a request to LCDd.

        @param command: The command to send to LCDd.
        @type command: string
        @param param: The parameters to send with the command
        @type param: string
        '''
        # Send the commend
        log.logger.debug("Request: " + command + ' ' + param)
        self.server.write((command + ' ' + param + "\n").encode())
        # Wait for return status
        response = self.poll()
        # wait for an acceptable answer
        while not self.check_response(response):
            response = self.poll()

    def check_response(self, response):
        if not response == None:
            if "success" in response:
                return(True)
            elif "huh" in response:
                return(True)

        return(False)

    def poll(self):
        '''
        Get the status from LCDd.
        '''
        log.logger.debug("Polling LCDd")
        # Check if server is ready for reading
        while  select([self.server], [], [], 0) == ([self.server], [], []):
            response = unquote(self.server.read_until(b"\n").decode())
            log.logger.debug("Response: " + response)
            # Do we understand the response
            if self.check_response(response):
                return response
            # Send the response on to the hook
            else:
                self.response_hook(response)

        return None

