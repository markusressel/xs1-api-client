from xs1_api_client import api_constants
from .base import XS1Actuator


class XS1Thermostat(XS1Actuator):
    """
    Represents a basic XS1 Actuator, there may be special variants for some types.
    """

    def __init__(self, state, api_interface):
        super(XS1Actuator, self).__init__(state, api_interface)

    def set_temperature(self, temp):
        """
        Sets the new target temperature of this thermostat

        :param temp: double value
        """
        response = self.api_interface.set_actuator_value(self.id(), temp)
        self.set_state(response[api_constants.NODE_ACTUATOR])
