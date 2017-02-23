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

    def __init__(self, host=None, user=None, password=None):
        """
        Creates a new api object.
        If no arguments are passed the global (shared) connection configuration will be used.
        Otherwise the connection info will only be used for this XS1 instance.
        """
        if not host and not user and not password:
            self.use_global_config = True
        else:
            self.use_global_config = False
            self.host = host
            self.user = user
            self.password = password

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
        :return:
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
        self.use_global_config = False
        self.host = host
        self.user = user
        self.password = password

    def use_global_connection_info(self):
        """
        Enables the use of global configuration data
        """
        self.use_global_config = True

    def send_request(self, command, *parameters):
        """Sends a GET request to the XS1 Gateway and returns the response as a JSON object.

        Keyword arguments:
        command -- command parameter for the URL
        parameters -- additional parameters needed for the specified command like 'number=3' (without any '&' symbol)
        """

        # decide if global or local configuration should be used
        if self.use_global_config:
            host = HOST
            user = USER
            password = PASSWORD
        else:
            host = self.host
            user = self.user
            password = self.password

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

        return json.loads(response_text)  # convert to json object

    def get_all_actuators(self):
        """Requests the list of actuators from the gateway."""

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
        """Requests the list of sensors from the gateway."""

        response = self.send_request(api_constants.COMMAND_GET_LIST_SENSORS)

        sensors = []

        if api_constants.NODE_SENSOR in response:
            for sensor in response[api_constants.NODE_SENSOR]:
                device = XS1Sensor(sensor, self)
                if device.enabled():
                    sensors.append(device)

        return sensors

    def get_state_actuator(self, actuator):
        """Refreshes the current value of the specified actuator.
        WARNING: this API is not very reliable, use subscribe instead

        Key parameters:
        actuator -- actuator to write the updated state to
        """
        response = self.send_request(api_constants.COMMAND_GET_STATE_ACTUATOR,
                                     api_constants.URL_PARAM_NUMBER + str(actuator.id()))

        actuator.set_json_state(response[api_constants.NODE_ACTUATOR])

        return actuator

    def get_state_sensor(self, sensor):
        """Refreshes the current value of the specified sensor.
        WARNING: this API is not very reliable, use subscribe instead

        Key parameters:
        sensor -- sensor to write the updated state to
        """
        response = self.send_request(api_constants.COMMAND_GET_STATE_SENSOR,
                                     api_constants.URL_PARAM_NUMBER + str(sensor.id()))

        sensor.set_json_state(response[api_constants.NODE_SENSOR])

        return sensor

    def call_actuator_function(self, actuator, function):
        """Excuted a function on the specified actuator.

        Key parameters:
        actuator -- actuator to execute the function on
        function -- id of the function to execute
        """

        # TODO: check if function exists
        response = self.send_request(api_constants.COMMAND_SET_STATE_ACTUATOR,
                                     api_constants.URL_PARAM_NUMBER + str(actuator.id()),
                                     api_constants.URL_PARAM_FUNCTION + str(function))

        actuator.set_json_state(response[api_constants.NODE_ACTUATOR])

        return actuator

    def set_actuator_value(self, actuator, value):
        """Sets a new value for the specified actuator.

        Key parameters:
        actuator -- actuator to set the new value on
        value -- the new value to set on the specified actuator
        """

        response = self.send_request(api_constants.COMMAND_SET_STATE_ACTUATOR,
                                     api_constants.URL_PARAM_NUMBER + str(actuator.id()),
                                     api_constants.URL_PARAM_VALUE + str(value))

        actuator.set_json_state(response[api_constants.NODE_ACTUATOR])

        return actuator

    def set_sensor_value(self, sensor, value):
        """Sets a new value for the specified sensor.
        WARNING: Only use this for "virtual" sensors or for debugging!

        Key parameters:
        sensor -- sensor to set the new value on
        value -- the new value to set on the specified sensor
        """
        response = self.send_request(api_constants.COMMAND_SET_STATE_SENSOR,
                                     api_constants.URL_PARAM_NUMBER + str(sensor.id()),
                                     api_constants.URL_PARAM_VALUE + str(value))

        sensor.set_json_state(response[api_constants.NODE_SENSOR])

        return response
