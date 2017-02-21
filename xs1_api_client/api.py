# -*- coding: utf-8 -*-
"""

Example usage:
    import mr.xs1
    xs1 = XS1()
    xs1.initialize('192.168.1.10', 'admin', 'secret') # one time init
    xs1.get_all_actuators()

"""

import logging

# networking
import requests
import json

from . import api_constants
from .device.actuator.base import XS1Actuator
from .device.actuator.switch import XS1Switch
from .device.sensor.base import XS1Sensor

_LOGGER = logging.getLogger(__name__)

HOST = ''
USER = ''
PASSWORD = ''


class XS1:
    """This class is the main api interface that handles all communication with the XS1 gateway.
    """

    def __init__(self, host, user, password):
        """Initializes api and connection info.

        Keyword arguments:
        host -- host address the gateway can be found at
        user -- username for authentication
        password -- password for authentication
        """
        global HOST
        global USER
        global PASSWORD

        HOST = str(host)
        USER = str(user)
        PASSWORD = str(password)

    def s(self):
        pass

    @staticmethod
    def send_request(command, *parameters):
        """Sends a GET request to the XS1 Gateway and returns the response as a JSON object.
        
        Keyword arguments:
        command -- command parameter for the URL
        parameters -- additional parameters needed for the specified command like 'number=3' (without any '&' symbol)
        """

        # create request url
        request_url = 'http://' + HOST + '/control?callback=callback'
        if USER and PASSWORD:
            request_url += '&' + api_constants.URL_PARAM_USER + USER + '&' + api_constants.URL_PARAM_PASSWORD + PASSWORD
        request_url += '&' + api_constants.URL_PARAM_COMMAND + command

        # append any additional parameters
        for parameter in parameters:
            request_url += '&' + parameter

        _LOGGER.info("request_url: " + request_url)

        # make request
        response = requests.get(request_url, auth=(USER, PASSWORD))
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
