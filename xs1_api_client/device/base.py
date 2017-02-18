from .. import api_constants

class XS1Device(object):
    """
    This is a generic XS1 device, all other objetcs inherit from this.
    """
    
    def __init__(self, device_state_json, api_interface):
        """
        Initializes the device.
        
        Keyword arguments:
        device_state_json -- json representation of this device (api response)
        api_interface -- the interface for handling api requests like fetching and setting values
        """
        self.api_interface = api_interface
        self.json_state = device_state_json
        
    def set_json_state(self, json):
        """Sets a new state for this device.
        
        Keyword arguments:
        device_state_json -- json representation of this device (api response)
        """
        self.json_state = json
        
    def id(self):
        """Returns the id of this device."""
        
        id = self.json_state.get(api_constants.NODE_PARAM_NUMBER)
        if id is None:
            id = self.json_state.get(api_constants.NODE_PARAM_ID)
        return id
    
    def type(self):
        """Returns the type of this device."""
        
        return self.json_state.get(api_constants.NODE_PARAM_TYPE)
    
    def name(self):
        """Returns the name of this device."""
        
        return self.json_state.get(api_constants.NODE_PARAM_NAME)
        
    def value(self):
        """Returns the current value of this device."""
        
        return self.json_state.get(api_constants.NODE_PARAM_VALUE)
        
    def new_value(self):
        """Returns the new value to set for this device.
        If this value differs from the currrent value the gateway is still trying to update the value on the device. If it does not differ the value has already been set.
        """
        return self.json_state.get(api_constants.NODE_PARAM_NEW_VALUE)
        
    def unit(self):
        """Returns the unit that is used for the value."""
        return self.json_state.get(api_constants.NODE_PARAM_UNIT)
        
    def last_update(self):
        """Returns the time when this device's value was updated last."""
        return self.json_state.get(api_constants.NODE_PARAM_UTIME)
        
    def set_value(self, value):
        """Sets a new value for this device.
        This method should be implemented by inheriting classes.
        """
        raise NotImplementedError("Not implemented!")
        
    def update(self):
        """Updates the current value of this device.
        This method should be implemented by inheriting classes.
        """
        raise NotImplementedError("Not implemented!")
        
    def enabled(self):
        """Returns if this device is enabled."""
        return not api_constants.VALUE_DISABLED in self.json_state[api_constants.NODE_PARAM_TYPE]