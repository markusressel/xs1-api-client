from .base import XS1Actuator
from ... import api_constants

class XS1Thermostat(XS1Actuator):
    """
    Represents a basic XS1 Actuator, there may be special variants for some types.
    """
    
    def __init__(self, device_state_json, api_interface):
        super(XS1Actuator, self).__init__(device_state_json, api_interface)
        
    def update(self):
        self.api_interface.get_state_actuator(self)
        
    def set_value(self, value):
        self.api_interface.set_actuator_value(self, value)
