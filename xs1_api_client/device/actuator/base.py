from ..base import XS1Device


class XS1Actuator(XS1Device):
    """
    Represents a basic XS1 Actuator, there may be special variants for some types.
    """

    def __init__(self, device_state_json, api_interface):
        super(XS1Actuator, self).__init__(device_state_json, api_interface)

    def update(self):
        """
        Updates the state of this actuator
        """
        self.api_interface.get_state_actuator(self)

    def set_value(self, value):
        """
        Sets a new value for this actuator

        :param value: new value to set
        """
        self.api_interface.set_actuator_value(self, value)
