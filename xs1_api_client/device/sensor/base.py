from ..base import XS1Device
from ... import api_constants

class XS1Sensor(XS1Device):
    """
    Represents a XS1 Sensor
    """
    
    def __init__(self, device_state_json, api_interface):
        super(XS1Sensor, self).__init__(device_state_json, api_interface)
        
    def update(self):
        self.api_interface.get_state_sensor(self)