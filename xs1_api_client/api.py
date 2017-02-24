# -*- coding: utf-8 -*-
"""
This is the main xs1_api_client api which contains the XS1 object to interact with the gateway.

Example usage can be found in the example.py file
"""

import json
import logging

import requests

from . import api_constants
from .device.actuator.base import XS1Actuator
from .device.actuator.switch import XS1Switch
from .device.sensor.base import XS1Sensor

_LOGGER = logging.getLogger(__name__)

# global config data
HOST = ''
USER = ''
PASSWORD = ''


class XS1:
    """
    This class is the main api interface that handles all communication with the XS1 gateway.
    """

    def __init__(self, host: str = None, user: str = None, password: str = None):
        """
        Creates a new api object.
        If no arguments are passed the global (shared) connection configuration will be used.
        Otherwise the connection info will only be used for this XS1 instance.

        :param host: host address of the gateway
        :param user: username for authentication
        :param password: password for authentication
        """

        if not host and not user and not password:
            self._use_global_config = True
        else:
            self._use_global_config = False
            self._host = host
            self._user = user
            self._password = password

        self._config_info = None

        self.update_config_info()

    @staticmethod
    def set_global_connection_info(host, user, password):
        """
        Sets the global connection info.
        This initialization is valid for all XS1 instances that do not have a specific connection configuration
        upon instantiation or using the set_connection_info() method.
        If you want a XS1 instance to use the global info instead of private use the use_global_connection_info() method.

        :param host: host address the gateway can be found at
        :param user: username for authentication
        :param password: password for authentication
        """

        global HOST
        global USER
        global PASSWORD

        HOST = str(host)
        USER = str(user)
        PASSWORD = str(password)

    def set_connection_info(self, host, user, password):
        """
        Sets private connection info for this XS1 instance.
        This XS1 instance will also immediately use this connection info.

        :param host: host address the gateway can be found at
        :param user: username for authentication
        :param password: password for authentication
        """

        self._use_global_config = False
        self._host = host
        self._user = user
        self._password = password

        self.update_config_info()

    def use_global_connection_info(self):
        """
        Enables the use of global configuration data
        """

        self._use_global_config = True
        self.update_config_info()  # update device info

    def send_request(self, command, *parameters):
        """
        Sends a GET request to the XS1 Gateway and returns the response as a JSON object.

        :param command: command parameter for the URL (see api_constants)
        :param parameters: additional parameters needed for the specified command like 'number=3' (without any '&' symbol)
        :return: the api response as a json object
        """

        # decide if global or local configuration should be used
        if self._use_global_config is True:
            host = HOST
            user = USER
            password = PASSWORD
        else:
            host = self._host
            user = self._user
            password = self._password

        # create request url
        request_url = 'http://' + host + '/control?callback=callback'
        if user and password:
            request_url += '&' + api_constants.URL_PARAM_USER + user + '&' + api_constants.URL_PARAM_PASSWORD + password
        request_url += '&' + api_constants.URL_PARAM_COMMAND + command

        # append any additional parameters
        for parameter in parameters:
            request_url += '&' + parameter

        _LOGGER.info("request_url: " + request_url)

        # make request
        response = requests.get(request_url, auth=(user, password))
        response_text = response.text  # .encode('utf-8')
        response_text = response_text[
                        response_text.index('{'):response_text.rindex('}') + 1]  # cut out valid json response

        response_dict = json.loads(response_text)  # convert to json object

        if api_constants.NODE_ERROR in response_dict:
            raise Exception(api_constants.ERROR_CODES[response_dict[api_constants.NODE_ERROR]])
        else:
            return response_dict

    def get_protocol_info(self):
        """
        Retrieves the protocol version that is used by the gateway

        :return: protocol version number
        """

        response = self.send_request(self, api_constants.COMMAND_GET_PROTOCOL_INFO)
        return response[api_constants.NODE_VERSION]

    def update_config_info(self):
        """
        Retrieves gateway specific (and immutable) configuration data
        """
        self._config_info = self.send_request(api_constants.COMMAND_GET_CONFIG_INFO)

    def get_gateway_name(self):
        """
        :return: the hostname of the gateway
        """
        return self._config_info[api_constants.NODE_INFO][api_constants.NODE_DEVICE_NAME]

    def get_gateway_hardware_version(self):
        """
        :return: the hardware version number of the gateway
        """
        return self._config_info[api_constants.NODE_INFO][api_constants.NODE_DEVICE_HARDWARE_VERSION]

    def get_gateway_bootloader_version(self):
        """
        :return: the bootloader version number of the gateway
        """
        return self._config_info[api_constants.NODE_INFO][api_constants.NODE_DEVICE_BOOTLOADER_VERSION]

    def get_gateway_firmware_version(self):
        """
        :return: the firmware version number of the gateway
        """
        return self._config_info[api_constants.NODE_INFO][api_constants.NODE_DEVICE_FIRMWARE_VERSION]

    def get_gateway_uptime(self):
        """
        :return: the uptime of the gateway in seconds
        """
        return self._config_info[api_constants.NODE_INFO][api_constants.NODE_DEVICE_UPTIME]

    def get_gateway_mac(self):
        """
        :return: the mac address of the gateway
        """
        return self._config_info[api_constants.NODE_INFO][api_constants.NODE_DEVICE_MAC]

    def get_all_actuators(self):
        """
        Requests the list of enabled actuators from the gateway.

        :return: a list of XS1Actuator objects
        """

        response = self.send_request(api_constants.COMMAND_GET_LIST_ACTUATORS)

        actuators = []
        if api_constants.NODE_ACTUATOR in response:
            # create actuator objects
            for actuator in response[api_constants.NODE_ACTUATOR]:
                if (actuator[api_constants.NODE_PARAM_TYPE] == api_constants.ACTUATOR_TYPE_SWITCH) or (
                            actuator[api_constants.NODE_PARAM_TYPE] == api_constants.ACTUATOR_TYPE_DIMMER):
                    device = XS1Switch(actuator, self)
                else:
                    device = XS1Actuator(actuator, self)

                if not device.enabled():
                    continue
                actuators.append(device)

        return actuators

    def get_all_sensors(self):
        """
        Requests the list of enabled sensors from the gateway.

        :return: list of XS1Sensor objects
        """

        response = self.send_request(api_constants.COMMAND_GET_LIST_SENSORS)

        sensors = []
        if api_constants.NODE_SENSOR in response:
            for sensor in response[api_constants.NODE_SENSOR]:
                device = XS1Sensor(sensor, self)
                if device.enabled():
                    sensors.append(device)

        return sensors

    def get_state_actuator(self, actuator_id):
        """
        Gets the current state of the specified actuator.

        :param actuator_id: actuator id
        :return: the api response as a dict
        """
        response = self.send_request(api_constants.COMMAND_GET_STATE_ACTUATOR,
                                     api_constants.URL_PARAM_NUMBER + str(actuator_id))

        return response[api_constants.NODE_ACTUATOR]

    def get_state_sensor(self, sensor_id):
        """
        Gets the current state of the specified sensor.

        :param sensor_id: sensor id
        :return: the api response as a dict
        """
        response = self.send_request(api_constants.COMMAND_GET_STATE_SENSOR,
                                     api_constants.URL_PARAM_NUMBER + str(sensor_id))

        return response[api_constants.NODE_SENSOR]

    def call_actuator_function(self, actuator, function):
        """
        Executes a function on the specified actuator and sets the response on the passed in actuator.

        :param actuator: actuator to execute the function on and set response value
        :param function: id of the function to execute
        :return: the passed in actuator
        """

        response = self.send_request(api_constants.COMMAND_SET_STATE_ACTUATOR,
                                     api_constants.URL_PARAM_NUMBER + str(actuator.id()),
                                     api_constants.URL_PARAM_FUNCTION + str(function))

        actuator.set_state(response[api_constants.NODE_ACTUATOR])

        return actuator

    def set_actuator_value(self, actuator_id, value):
        """
        Sets a new value for the specified actuator.

        :param actuator_id: actuator id to set the new value on
        :param value: the new value to set on the specified actuator
        :return: the passed in XS1Actuator object
        """

        response = self.send_request(api_constants.COMMAND_SET_STATE_ACTUATOR,
                                     api_constants.URL_PARAM_NUMBER + str(actuator_id),
                                     api_constants.URL_PARAM_VALUE + str(value))

        return response[api_constants.NODE_ACTUATOR]

    def set_sensor_value(self, sensor_id, value):
        """
        Sets a new value for the specified sensor.
        WARNING: Only use this for "virtual" sensors or for debugging!

        :param sensor_id: sensor id to set the new value on
        :param value: the new value to set on the specified sensor
        :return: the passed in XS1Sensor object
        """

        response = self.send_request(api_constants.COMMAND_SET_STATE_SENSOR,
                                     api_constants.URL_PARAM_NUMBER + str(sensor_id),
                                     api_constants.URL_PARAM_VALUE + str(value))

        return response[api_constants.NODE_SENSOR]
