import re

from xs1_api_client.api_constants import Node, ActuatorType, SensorType


class XS1Device(object):
    """
    This is a generic XS1 device, all other objetcs inherit from this.
    """

    NAME_PATTERN_VALID = re.compile(r'^[a-zA-Z0-9_]+$', re.IGNORECASE)

    def __init__(self, state: dict, api) -> None:
        """
        Initializes the device.

        :param state: json representation of this device (api response)
        :param api: the interface for handling api requests like fetching and setting values
        """
        self._api_interface = api
        self._state = state

    def __str__(self) -> str:
        """
        :return: String representation of this device
        """
        return "%s (ID: %i, Number: %i, Enabled: %s, Type: %s, Value: %s, New Value: %s, Unit: %s)" % (
            self.name(), self.id(), self.number(), self.enabled(), self.type(), self.value(), self.new_value(),
            self.unit())

    def set_state(self, new_state: dict) -> None:
        """
        Sets a new state for this device.
        If there is an existing state, new and old values will be merged
        to retain any information that was missing from api responses.

        :param new_state: new representation of this device (api response)
        """
        if self._state:
            for key, value in new_state.items():
                self._state[key] = value

                #  self._state = {**self._state, **new_state}  # merge dicts (Python 3.5 required)
        else:
            self._state = new_state  # set initial state

    def id(self) -> int:
        """
        :return: id of this device
        """
        return self._get_node_value(self._state, Node.PARAM_ID)

    def number(self) -> int:
        """
        :return: number of this device
        """
        return self._get_node_value(self._state, Node.PARAM_NUMBER)

    def type(self) -> ActuatorType or SensorType or str:
        """
        :return: the type of this device
        """
        device_type_string = self._get_node_value(self._state, Node.PARAM_TYPE)

        # try to convert string value to Enum constant
        try:
            return ActuatorType(device_type_string)
        except ValueError:
            pass

        try:
            return SensorType(device_type_string)
        except ValueError:
            pass

        return device_type_string

    def name(self) -> str:
        """
        :return: the name of this device
        """
        return self._get_node_value(self._state, Node.PARAM_NAME)

    def set_name(self, name: str):
        """
        Sets a new name for this device.
        Keep in mind that there are some limitations for a device name.

        :param name: the new name to set
        :return: the new name of the actuator
        """
        if not self.NAME_PATTERN_VALID.match(name):
            raise AttributeError("Name must be alphanumeric + underscore!")

    def value(self):
        """
        :return: the current value of this device
        """
        return self._get_node_value(self._state, Node.PARAM_VALUE)

    def new_value(self):
        """
        Returns the new value to set for this device.
        If this value differs from the currrent value the gateway is still trying to update the value on the device.
        If it does not differ the value has already been set.

        :return: the new value to set for this device
        """
        return self._get_node_value(self._state, Node.PARAM_NEW_VALUE)

    def unit(self) -> str:
        """
        :return: the unit that is used for the value
        """
        return self._get_node_value(self._state, Node.PARAM_UNIT)

    def last_update(self) -> int:
        """
        :return: the time when this device's value was updated last
        """
        return self._get_node_value(self._state, Node.PARAM_UTIME)

    def set_value(self, value) -> None:
        """
        Sets a new value for this device.
        This method should be implemented by inheriting classes.

        :param value: the new value to set
        """
        raise NotImplementedError("Not implemented!")

    def update(self) -> None:
        """
        Updates the current value of this device.
        This method should be implemented by inheriting classes.
        """
        raise NotImplementedError("Not implemented!")

    def enabled(self) -> bool:
        """
        :return: Returns if this device is enabled.
        """
        return not ActuatorType.DISABLED == self.type()

    def _get_node_value(self, dictionary: dict, node: Node or str) -> str or None:
        """
        :param dictionary: the dictionary used for lookup
        :param node: the node to search for and retrieve its value
        :return: the value of the specified node or None if it doesn't exist
        """
        if isinstance(node, Node):
            node_name = node.value
        else:
            node_name = str(node)

        return dictionary.get(node_name)
