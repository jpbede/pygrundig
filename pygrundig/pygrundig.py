import logging
import requests
import json
from enum import Enum

TIMEOUT = 10
_LOGGER = logging.getLogger(__name__)

class PyGrundig:

    class KeyCode(Enum):
        POWER = "-2544:-4081"
        MUTE = "-2539:-4018"
        VOL_UP = "-2475:-4020"
        VOL_DOWN = "-2476:-4019"
        PROGRAM_UP = "-2464:-4026"
        PROGRAM_DOWN = "-2465:-4025"

    class ServiceType(Enum):
        DTV = "DTV"
        ATV = "ATV"
        RADIO = "Radio"
        DATA = "Data"

    def __init__(self, host, port="8085"):
        """Initialize the Grundig TV class."""

        self._host = host
        self._port = port

    def _send_get_request(self, path, log_errors=True):
        """ Send request command via HTTP json to Grundig TV."""
        try:
            response = requests.get('http://' + self._host + ':' + self._port + path,
                                    headers={},
                                    timeout=TIMEOUT)

        except Exception as exception_instance:
            return False

        else:
            return response.content.decode('utf-8')

    def send_key_command(self, key_command):
        if key_command not in self.KeyCode:
            raise ValueError('key code not valid')

        parts = str.split(key_command.value, ":")
        response = self._send_get_request("/sendrcpackage?keyid=" + parts[0] + "&keysymbol=" + parts[1])
        if response and "Set rc key is handled for" in response:
            return True
        else:
            return False

    def get_current_channel(self):
        result = self._send_get_request("/getchannel")
        if result:
            pjson = json.loads(result)
            return pjson["channel"]
        return False

    def set_channel(self, channelNumber, serviceType):
        if serviceType not in self.ServiceType:
            raise ValueError('service type not valid')

        response = self._send_get_request("/setchannel?no="+channelNumber+"&service="+serviceType.value)
        return response == 'CHANNEL SET TO'

    def get_current_running_progam_list(self):
        result = self._send_get_request("/nowlist")
        if result:
            return json.loads(result)
        return False

    def get_current_running_program(self):
        channel = self.get_current_channel()
        if channel:
            channelNumber = channel["channelNumber"]
            running_list = self.get_current_running_list()
            if running_list:
                running_list = running_list["eventList"]
                for running in running_list:
                    runningChannelNumber = running["channel"]["channelNumber"]
                    if runningChannelNumber == channelNumber:
                        return running
        return False

    def get_channel_list(self):
        channeljson = self.get_current_running_list()
        if channeljson:
            channels = []
            events = channeljson["eventList"]
            for event in events:
                channels.append(event["channel"])
            return channels
        return False

    def toggle_mute(self):
        return self.send_key_command(self.KeyCode.MUTE)

    def power_off(self):
        return self.send_key_command(self.KeyCode.POWER)