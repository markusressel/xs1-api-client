# -*- coding: utf-8 -*-
"""
This is the main xs1_api_client api which contains the XS1 object to interact with the gateway.

Example usage can be found in the example.py file
"""

import json
import logging

import requests

from xs1_api_client.api_constants import UrlParam, Command, Node, ActuatorType, ErrorCode
from xs1_api_client.device.actuator import XS1Actuator
from xs1_api_client.device.actuator.switch import XS1Switch
from xs1_api_client.device.sensor import XS1Sensor

_LOGGER = logging.getLogger(__name__)


class XS1:
    """
    This class is the main api interface that handles all communication with the XS1 gateway.
    """

    def __init__(self, host: str = None, user: str = None, password: str = None) -> None:
        """
        Creates a new api object.

        :param host: host address of the gateway
        :param user: username for authentication
        :param password: password for authentication
        """

        self._host = None
        self._user = None
        self._password = None
        self._config_info = None

        self.set_connection_info(host, user, password)

    def set_connection_info(self, host, user, password) -> None:
        """
        Sets private connection info for this XS1 instance.
        This XS1 instance will also immediately use this connection info.

        :param host: host address the gateway can be found at
        :param user: username for authentication
        :param password: password for authentication
        """

        self._host = host
        self._user = user
        self._password = password

        self.update_config_info()

    def send_request(self, command: Command, parameters: dict = None) -> dict:
        """
        Sends a GET request to the XS1 Gateway and returns the response as a JSON object.

        :param command: command parameter for the URL (see api_constants)
        :param parameters: additional parameters needed for the specified command like 'number=3' passed in as a dictionary
        :return: the api response as a json object
        """

        host = self._host
        user = self._user
        password = self._password

        # create request url
        request_url = 'http://' + host + '/control?callback=callback'
        # append credentials, if any
        if user and password:
            request_url += '&' + UrlParam.USER.value + '=' + user + '&' + UrlParam.PASSWORD.value + '=' + password
        # append command to execute
        request_url += '&' + UrlParam.COMMAND.value + '=' + command.value

        # append any additional parameters
        if parameters:
            for key, value in parameters.items():
                if not isinstance(key, UrlParam):
                    raise Exception("Invalid type of parameter key! Needs to be of type UrlParam!")
                request_url += '&' + key.value + '=' + str(value)

        _LOGGER.info("request_url: " + request_url)

        # make request
        response = requests.get(request_url, auth=(user, password))
        response_text = response.text  # .encode('utf-8')
        response_text_json = response_text[
                             response_text.index('{'):response_text.rindex('}') + 1]  # cut out valid json response

        response_dict = json.loads(response_text_json)  # convert to json object

        error = self._get_node_value(response_dict, Node.ERROR)
        if error:
            try:
                error_code = ErrorCode(error)
                error_message = ErrorCode.get_message(error_code)
            except ValueError:
                error_code = "UNKNOWN"
                error_message = "Unknown error code " + str(error)

            parameters_message = ""
            if parameters:
                for key, value in parameters.items():
                    parameters_message += str(key) + "=" + str(value) + ", "

            raise Exception(
                str(error_code) + ": " + error_message +
                " while trying to execute " + str(command) +
                " with " + parameters_message[:-2])
        else:
            return response_dict

    def get_protocol_info(self) -> str:
        """
        Retrieves the protocol version that is used by the gateway

        :return: protocol version number
        """

        response = self.send_request(Command.GET_PROTOCOL_INFO)
        return self._get_node_value(response, Node.VERSION)

    def update_config_info(self) -> None:
        """
        Retrieves gateway specific (and immutable) configuration data
        """
        self._config_info = self.send_request(Command.GET_CONFIG_INFO)

    def get_gateway_name(self) -> str:
        """
        :return: the hostname of the gateway
        """
        return self._get_config_info_value(Node.DEVICE_NAME)

    def get_gateway_hardware_version(self) -> str:
        """
        :return: the hardware version number of the gateway
        """
        return self._get_config_info_value(Node.DEVICE_HARDWARE_VERSION)

    def get_gateway_bootloader_version(self) -> str:
        """
        :return: the bootloader version number of the gateway
        """
        return self._get_config_info_value(Node.DEVICE_BOOTLOADER_VERSION)

    def get_gateway_firmware_version(self) -> str:
        """
        :return: the firmware version number of the gateway
        """
        return self._get_config_info_value(Node.DEVICE_FIRMWARE_VERSION)

    def get_gateway_uptime(self) -> str:
        """
        :return: the uptime of the gateway in seconds
        """
        return self._get_config_info_value(Node.DEVICE_UPTIME)

    def get_gateway_mac(self) -> str:
        """
        :return: the mac address of the gateway
        """
        return self._get_config_info_value(Node.DEVICE_MAC)

    def _get_config_info_value(self, node: Node):
        return self._config_info[Node.INFO.value][node.value]

    def get_all_actuators(self, enabled: bool or None = None) -> [XS1Actuator]:
        """
        Requests the list of enabled actuators from the gateway.

        :param enabled:
        :return: a list of XS1Actuator objects
        """

        response = self.send_request(Command.GET_LIST_ACTUATORS)

        all_actuators = []
        # create actuator objects
        for actuator in self._get_node_value(response, Node.ACTUATOR):
            if (self._get_node_value(actuator, Node.PARAM_TYPE) == ActuatorType.SWITCH) or (
                        self._get_node_value(actuator, Node.PARAM_TYPE) == ActuatorType.DIMMER
            ):
                device = XS1Switch(actuator, self)
            else:
                device = XS1Actuator(actuator, self)

            all_actuators.append(device)

        if enabled is None:
            return all_actuators
        else:
            filtered_actuators = []
            for actuator in all_actuators:
                if actuator.enabled() != enabled:
                    continue
                filtered_actuators.append(actuator)
            return filtered_actuators

    def get_all_sensors(self, enabled: bool or None = None) -> [XS1Sensor]:
        """
        Requests the list of enabled sensors from the gateway.

        :return: list of XS1Sensor objects
        """

        response = self.send_request(Command.GET_LIST_SENSORS)

        all_sensors = []
        for sensor in self._get_node_value(response, Node.SENSOR):
            device = XS1Sensor(sensor, self)
            all_sensors.append(device)

        if enabled is None:
            return all_sensors
        else:
            filtered_sensors = []
            for sensor in all_sensors:
                if sensor.enabled() != enabled:
                    continue
                filtered_sensors.append(sensor)
            return filtered_sensors

    def get_state_actuator(self, actuator_id) -> dict:
        """
        Gets the current state of the specified actuator.

        :param actuator_id: actuator id
        :return: the api response as a dict
        """
        return self.send_request(Command.GET_STATE_ACTUATOR,
                                 {UrlParam.NUMBER: actuator_id})

    def get_state_sensor(self, sensor_id) -> dict:
        """
        Gets the current state of the specified sensor.

        :param sensor_id: sensor id
        :return: the api response as a dict
        """
        return self.send_request(Command.GET_STATE_SENSOR,
                                 {
                                     UrlParam.NUMBER: sensor_id,
                                 })

    def call_actuator_function(self, actuator_id, function) -> dict:
        """
        Executes a function on the specified actuator and sets the response on the passed in actuator.

        :param actuator_id: actuator id to execute the function on and set response value
        :param function: id of the function to execute
        :return: the api response
        """
        return self.send_request(Command.SET_STATE_ACTUATOR,
                                 {
                                     UrlParam.NUMBER: actuator_id,
                                     UrlParam.FUNCTION: function
                                 })

    def set_actuator_value(self, actuator_id, value) -> dict:
        """
        Sets a new value for the specified actuator.

        :param actuator_id: actuator id to set the new value on
        :param value: the new value to set on the specified actuator
        :return: the api response
        """

        return self.send_request(Command.SET_STATE_ACTUATOR,
                                 {
                                     UrlParam.NUMBER: actuator_id,
                                     UrlParam.VALUE: value
                                 })

    def set_sensor_value(self, sensor_id, value) -> dict:
        """
        Sets a new value for the specified sensor.
        WARNING: Only use this for "virtual" sensors or for debugging!

        :param sensor_id: sensor id to set the new value on
        :param value: the new value to set on the specified sensor
        :return: the api response
        """

        return self.send_request(Command.SET_STATE_SENSOR,
                                 {
                                     UrlParam.NUMBER: sensor_id,
                                     UrlParam.VALUE: value
                                 })

    def _get_node_value(self, dictionary: dict, node: Node) -> str or None:
        """
        :param dictionary: the dictionary for lookup
        :param node: the node to retrieve the value for
        :return: the value of this node or None if it doesn't exist
        """
        return dictionary.get(node.value)
