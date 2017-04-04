from xs1_api_client import api_constants, XS1
from ..base import XS1Device


class XS1Sensor(XS1Device):
    """
    Represents a XS1 Sensor
    """

    def __init__(self, state, api: XS1):
        super(XS1Sensor, self).__init__(state, api)

    def update(self) -> None:
        """
        Updates the state of this sensor
        """
        response = self._api_interface.get_state_sensor(self.id())
        self.set_state(response[api_constants.NODE_SENSOR])

    def set_value(self, value) -> None:
        """
        Sets a value for this sensor
        This should only be used for debugging purpose!
        :param value: new value to set
        """
        response = self._api_interface.set_sensor_value(self.id(), value)
        self.set_state(response[api_constants.NODE_SENSOR])
