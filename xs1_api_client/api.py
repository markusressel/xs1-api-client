# -*- coding: utf-8 -*-
"""
This is the main xs1_api_client api which contains the XS1 object to interact with the gateway.

Example usage can be found in the example.py file
"""

import json
import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from xs1_api_client.api_constants import UrlParam, Command, Node, ActuatorType, ErrorCode, ApiConstant
from xs1_api_client.device.actuator import XS1Actuator
from xs1_api_client.device.actuator.switch import XS1Switch
from xs1_api_client.device.sensor import XS1Sensor

_LOGGER = logging.getLogger(__name__)


class XS1:
    """
    This class is the main api interface that handles all communication with the XS1 gateway.
    """

    # setup retry and backoff strategy
    RETRY_STRATEGY = Retry(total=5,
                           backoff_factor=0.1,
                           status_forcelist=[500, 502, 503, 504])

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

        if host:
            self.update_config_info()

    def call_api(self, command: Command, parameters: dict = None) -> dict:
        """
        Executes a command on the xs1 api and returns it's response as a dictionary (if there was no error).

        :param command: command parameter for the URL (see api_constants)
        :param parameters: additional parameters needed for the specified command like 'number=3' passed in as a dictionary
        :return: the api response
        """

        request_url = self._build_request_url(command, parameters)
        response = self._send_request(request_url)

        # raises an exception if anything is wrong
        self._check_errors(command, parameters, response)

        return response

    def _build_request_url(self, command: Command, parameters: dict = None) -> str:
        """
        Builds a request url from the input parameters

        :param command: the main command
        :param parameters: additional parameters
        :return: request url
        """

        # create request url
        request_url = "http://%s/control?callback=callback" % self._host
        # append credentials, if any
        if self._user and self._password:
            request_url += "&%s=%s&%s=%s" % (UrlParam.USER.value, self._user, UrlParam.PASSWORD.value, self._password)
        # append command to execute
        if isinstance(command, Command):
            command = command.value
        elif isinstance(command, str):
            command = str(command)
        else:
            raise ValueError("Invalid command type! Must be a Command enum constant or a string!")

        request_url += "&%s=%s" % (UrlParam.COMMAND.value, command)

        # append any additional parameters
        if parameters:

            def process_parameters(params: dict) -> dict:
                """
                Removes duplicates and replaces ApiConstants (Enums) with it's value

                :param params: parameters to process
                :return: cleaned up parameters
                """

                processed = {}
                for k, v in params.items():
                    # special treatment when a list of functions is found
                    if k == UrlParam.FUNCTION and isinstance(v, list):
                        for idx, func in enumerate(v):
                            function_type = None
                            function_description = None

                            for k2, v2 in func.items():
                                if k2 == "type":
                                    function_type = v2
                                if k2 == "dsc":
                                    function_description = v2

                            if isinstance(function_type, ApiConstant):
                                function_type = function_type.value
                            if isinstance(function_description, ApiConstant):
                                function_description = function_description.value

                            processed['function%d.type' % (idx + 1)] = str(function_type)
                            processed['function%d.dsc' % (idx + 1)] = str(function_description)

                        continue

                    # if the value is an enum, use it's value instead
                    if isinstance(v, ApiConstant):
                        v = v.value

                    # if the key is an enum, use it's value as the key
                    # and give it priority over other parameters that might have the same key
                    if isinstance(k, ApiConstant):
                        processed[k.value] = v
                    else:
                        k = str(k)
                        if k not in processed:
                            processed[k] = v

                return processed

            processed_params = process_parameters(parameters)
            for key, value in processed_params.items():
                # append parameter to request url
                request_url += "&%s=%s" % (key, value)

        return request_url

    def _send_request(self, request_url: str) -> dict:
        """
        Sends a GET request to the XS1 Gateway and returns the response as a JSON object.

        :param request_url: the request url
        :return: the api response as a json object
        """

        _LOGGER.info("request_url: " + request_url)

        # create session
        session = requests.Session()
        session.mount('http://', HTTPAdapter(max_retries=self.RETRY_STRATEGY))

        # make request
        response = session.get(request_url, auth=(self._user, self._password))
        response_text = response.text  # .encode('utf-8')
        response_text_json = response_text[
                             response_text.index('{'):response_text.rindex('}') + 1]  # cut out valid json response

        response_dict = json.loads(response_text_json)  # convert to json object
        return response_dict

    def _check_errors(self, command: Command, parameters: dict, response: dict) -> dict:
        """
        Checks the repsonse dict for errors.
        Does nothing if no error is detected

        :param command: the command used for the request
        :param parameters: parameters used for the request
        :param response: the api response json
        :return: the api response if no error is detected, raises an exception otherwise
        """

        error = self._get_node_value(response, Node.ERROR)
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
            return response

    def get_protocol_info(self) -> str:
        """
        Retrieves the protocol version that is used by the gateway

        :return: protocol version number
        """

        response = self.call_api(Command.GET_PROTOCOL_INFO)
        return self._get_node_value(response, Node.VERSION)

    def update_config_info(self) -> None:
        """
        Retrieves gateway specific (and immutable) configuration data
        """
        self._config_info = self.call_api(Command.GET_CONFIG_INFO)

    def get_config_main(self) -> dict:
        """
        :return: main configuration of the XS1
        """
        response = self.call_api(Command.GET_CONFIG_MAIN)
        return self._get_node_value(response, "main")

    def get_list_systems(self) -> list:
        """
        :return: a list of currently compatible systems
        """
        response = self.call_api(Command.GET_LIST_SYSTEMS)
        return self._get_node_value(response, Node.SYSTEM)

    def get_list_functions(self) -> list:
        """
        :return: a list of available functions / actions for actuators
        """
        response = self.call_api(Command.GET_LIST_FUNCTIONS)
        return self._get_node_value(response, Node.FUNCTION)

    def get_types_actuators(self) -> list:
        """
        :return: a list of compatible actuators
        """
        response = self.call_api(Command.GET_TYPES_ACTUATORS)
        return self._get_node_value(response, "actuatortype")

    def get_types_sensors(self) -> list:
        """
        :return: a list of compatible sensors
        """
        response = self.call_api(Command.GET_TYPES_SENSORS)
        return self._get_node_value(response, "sensortype")

    def get_config_actuator(self, actuator_id: int) -> dict:
        """
        :return: the configuration of a specific actuator
        """
        response = self.call_api(Command.GET_CONFIG_ACTUATOR, {UrlParam.NUMBER: actuator_id})
        return self._get_node_value(response, Node.ACTUATOR)

    def set_config_actuator(self, actuator_id: int, configuration: dict) -> dict:
        """
        :return: the configuration of a specific actuator
        """

        configuration[UrlParam.NUMBER] = actuator_id

        response = self.call_api(Command.SET_CONFIG_ACTUATOR, configuration)
        return self._get_node_value(response, Node.ACTUATOR)

    def get_config_sensor(self, sensor_id: int) -> dict:
        """
        :return: the configuration of a specific sensor
        """
        response = self.call_api(Command.GET_CONFIG_SENSOR, {UrlParam.NUMBER: sensor_id})
        return self._get_node_value(response, Node.SENSOR)

    def set_config_sensor(self, sensor_id: int, configuration: dict) -> dict:
        """
        :return: the configuration of a specific actuator
        """

        configuration[UrlParam.NUMBER.value] = sensor_id

        response = self.call_api(Command.SET_CONFIG_SENSOR, configuration)
        return self._get_node_value(response, Node.SENSOR)

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

    def get_gateway_uptime(self) -> int:
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

    def get_actuator(self, actuator_id: int) -> XS1Actuator or None:
        """
        Get an actuator with a specific id
        :param actuator_id: the id of the actuator
        :return: XS1Actuator
        """

        all_actuators = self.get_all_actuators()
        for actuator in all_actuators:
            if actuator.id() == actuator_id:
                return actuator

        return None

    def get_all_actuators(self, enabled: bool or None = None) -> [XS1Actuator]:
        """
        Requests the list of enabled actuators from the gateway.

        :param enabled:
        :return: a list of XS1Actuator objects
        """

        response = self.call_api(Command.GET_LIST_ACTUATORS)

        all_actuators = []
        # create actuator objects
        for actuator in self._get_node_value(response, Node.ACTUATOR):
            actuator_type = self._get_node_value(actuator, Node.PARAM_TYPE)
            if ActuatorType.SWITCH == actuator_type or ActuatorType.DIMMER == actuator_type:
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

    def get_sensor(self, sensor_id: int) -> XS1Sensor or None:
        """
        Get a sensor with a specific id
        :param sensor_id: the id of the actuator
        :return: XS1Sensor
        """

        all_sensors = self.get_all_sensors()
        for sensor in all_sensors:
            if sensor.id() == sensor_id:
                return sensor

        return None

    def get_all_sensors(self, enabled: bool or None = None) -> [XS1Sensor]:
        """
        Requests the list of enabled sensors from the gateway.

        :return: list of XS1Sensor objects
        """

        response = self.call_api(Command.GET_LIST_SENSORS)

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
        return self.call_api(Command.GET_STATE_ACTUATOR,
                             {UrlParam.NUMBER: actuator_id})

    def get_state_sensor(self, sensor_id) -> dict:
        """
        Gets the current state of the specified sensor.

        :param sensor_id: sensor id
        :return: the api response as a dict
        """
        return self.call_api(Command.GET_STATE_SENSOR,
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

        return self.call_api(Command.SET_STATE_ACTUATOR,
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

        return self.call_api(Command.SET_STATE_ACTUATOR,
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

        return self.call_api(Command.SET_STATE_SENSOR,
                             {
                                 UrlParam.NUMBER: sensor_id,
                                 UrlParam.VALUE: value
                             })

    def _get_node_value(self, dictionary: dict, node: Node or str) -> any:
        """
        :param dictionary: the dictionary for lookup
        :param node: the node to retrieve the value for
        :return: the value of this node or None if it doesn't exist
        """

        if isinstance(node, Node):
            node_name = node.value
        else:
            node_name = str(node)

        return dictionary.get(node_name)
