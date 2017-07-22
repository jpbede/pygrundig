import logging
import base64
import collections
import socket
import struct
import requests
import json

TIMEOUT = 10

_LOGGER = logging.getLogger(__name__)


class PyGrundig:

    def __init__(self, host, port="8085"):
        """Initialize the Grundig TV class."""

        self._host = host
        self._port = port

    def send_get_request(self, path, log_errors=True):
        """ Send request command via HTTP json to Grundig TV."""

        try:
            response = requests.get('http://' + self._host + ':' + self._port + '/' + path,
                                    headers={},
                                    timeout=TIMEOUT)

        except requests.exceptions.HTTPError as exception_instance:
            if log_errors:
                _LOGGER.error("HTTPError: " + str(exception_instance))

        except Exception as exception_instance:
            if log_errors:
                _LOGGER.error("Exception: " + str(exception_instance))

        else:
            return response.content.decode('utf-8')

    def _bsr(self,value, bits):
        """ bsr(value, bits) -> value shifted right by bits

        This function is here because an expression in the original java
        source contained the token '>>>' and/or '>>>=' (bit shift right
        and/or bit shift right assign).  In place of these, the python
        source code below contains calls to this function.

        Copyright 2003 Jeffrey Clement.  See pyrijnadel.py for license and
        original source.
        """
        minint = -2147483648
        if bits == 0:
            return value
        elif bits == 31:
            if value & minint:
                return 1
            else:
                return 0
        elif bits < 0 or bits > 31:
            raise ValueError('bad shift count')
        tmp = (value & 0x7FFFFFFE) // 2 ** bits
        if (value & minint):
            return (tmp | (0x40000000 // 2 ** (bits - 1)))
        else:
            return tmp

    def _keyCodeToByteArray(self, arg1, arg2):
        tmp1 = int((self._bsr((int(arg1)), 8)))
        tmp2 = int((self._bsr((int(arg2)), 8)))
        return bytes([int(arg1), tmp1, int(arg2), tmp2])

    def get_current_channel(self):
        pjson = json.loads(self.send_get_request("/getchannel"))
        return pjson["channel"]

    def set_channel(self, channelNumber, serviceType):
        response = self.send_get_request("/setchannel?no="+channelNumber+"&service="+serviceType)
        return response == 'CHANNEL SET TO'

    def get_current_running_list(self):
        rjson = json.loads(self.send_get_request("/nowlist"))
        return rjson

    def get_channel_list(self):
        channeljson = self.get_current_running_list()
        channels = []
        events = channeljson["eventList"]
        for event in events:
            channels.append(event["channel"])

        return channels

    def send_key_command(self):
        responsejson = self.send_get_request("/sendrcpackage?keyid=&keysymbol=")

    def toggle_mute(self):
        return False