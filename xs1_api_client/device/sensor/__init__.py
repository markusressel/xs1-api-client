from xs1_api_client.api_constants import Node
from xs1_api_client.device import XS1Device


class XS1Sensor(XS1Device):
    """
    Represents a XS1 Sensor
    """

    def __init__(self, state, api):
        super(XS1Sensor, self).__init__(state, api)

    def __str__(self):
        return "Sensor: " + super(XS1Sensor, self).__str__()

    def update(self) -> None:
        """
        Updates the state of this sensor
        """
        response = self._api_interface.get_state_sensor(self.number())
        new_value = self._get_node_value(response, Node.SENSOR)
        self.set_state(new_value)

    def set_name(self, name: str):
        """
        Sets a new name for this device.
        Keep in mind that there are some limitations for a device name.
        :param name: the new name to set
        :return: the new name of the sensor
        """
        # check name arg for validity
        super(XS1Sensor, self).set_name(name)

        config = self._api_interface.get_config_sensor(self.number())

        # name is already set, to minimize flash writes don't write it again
        if config["name"] == name:
            return name

        config["name"] = name

        result = self._api_interface.set_config_sensor(self.number(), config)
        new_name = self._get_node_value(result, "name")

        # save new_name to internal state
        self._state[Node.PARAM_NAME.value] = new_name

        return new_name

    def set_value(self, value) -> None:
        """
        Sets a value for this sensor
        This should only be used for debugging purpose!
        :param value: new value to set
        """
        response = self._api_interface.set_sensor_value(self.number(), value)
        new_value = self._get_node_value(response, Node.SENSOR)
        self.set_state(new_value)
