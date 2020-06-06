from xs1_api_client.api_constants import Node
from xs1_api_client.device.actuator import XS1Actuator


class XS1Switch(XS1Actuator):
    """
    Represents a XS1 Switch.
    """

    def __init__(self, state, api):
        """Initializes the switch."""
        super(XS1Switch, self).__init__(state, api)

    def turn_on(self) -> None:
        """Turns on the switch."""
        response = self._api_interface.set_actuator_value(self.number(), 100)
        new_value = self._get_node_value(response, Node.ACTUATOR)
        self.set_state(new_value)

    def turn_off(self) -> None:
        """Turns off the switch."""
        response = self._api_interface.set_actuator_value(self.number(), 0)
        new_value = self._get_node_value(response, Node.ACTUATOR)
        self.set_state(new_value)
