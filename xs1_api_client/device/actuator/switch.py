from xs1_api_client import api_constants
from .base import XS1Actuator


class XS1Switch(XS1Actuator):
    """
    Represents a XS1 Switch.
    """

    def __init__(self, state, api_interface):
        """Initializes the switch."""
        super(XS1Switch, self).__init__(state, api_interface)

    def turn_on(self):
        """Turns on the switch."""
        response = self.api_interface.set_actuator_value(self.id(), 100)
        self.set_state(response[api_constants.NODE_ACTUATOR])

    def turn_off(self):
        """Turns off the switch."""
        response = self.api_interface.set_actuator_value(self.id(), 0)
        self.set_state(response[api_constants.NODE_ACTUATOR])
