from ..base import XS1Device


class XS1Sensor(XS1Device):
    """
    Represents a XS1 Sensor
    """

    def __init__(self, state, api_interface):
        super(XS1Sensor, self).__init__(state, api_interface)

    def update(self):
        """
        Updates the state of this sensor
        """
        state = self.api_interface.get_state_sensor(self.id())
        self.set_state(state)

    def set_value(self, value):
        """
        Sets a value for this sensor
        This should only be used for debugging purpose!
        :param value: new value to set
        """
        new_state = self.api_interface.set_sensor_value(self.id(), value)
        self.set_state(new_state)
