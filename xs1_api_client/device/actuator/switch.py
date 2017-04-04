from xs1_api_client import api_constants
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
        response = self._api_interface.set_actuator_value(self.id(), 100)
        self.set_state(response[api_constants.NODE_ACTUATOR])

    def turn_off(self) -> None:
        """Turns off the switch."""
        response = self._api_interface.set_actuator_value(self.id(), 0)
        self.set_state(response[api_constants.NODE_ACTUATOR])
