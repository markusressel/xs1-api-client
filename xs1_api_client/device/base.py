from .. import api_constants


class XS1Device(object):
    """
    This is a generic XS1 device, all other objetcs inherit from this.
    """

    def __init__(self, device_state_json, api_interface):
        """
        Initializes the device.

        :param device_state_json: json representation of this device (api response)
        :param api_interface: the interface for handling api requests like fetching and setting values
        """
        self.api_interface = api_interface
        self.json_state = device_state_json

    def set_json_state(self, json):
        """
        Sets a new state for this device.

        :param json: json representation of this device (api response)
        :return:
        """
        self.json_state = json

    def id(self):
        """
        :return: id of this device
        """
        device_id = self.json_state.get(api_constants.NODE_PARAM_NUMBER)
        if device_id is None:
            device_id = self.json_state.get(api_constants.NODE_PARAM_ID)
        return device_id

    def type(self):
        """
        :return: the type of this device
        """
        return self.json_state.get(api_constants.NODE_PARAM_TYPE)

    def name(self):
        """
        :return: the name of this device
        """
        return self.json_state.get(api_constants.NODE_PARAM_NAME)

    def value(self):
        """
        :return: the current value of this device
        """
        return self.json_state.get(api_constants.NODE_PARAM_VALUE)

    def new_value(self):
        """
        Returns the new value to set for this device.
        If this value differs from the currrent value the gateway is still trying to update the value on the device.
        If it does not differ the value has already been set.

        :return: the new value to set for this device
        """
        return self.json_state.get(api_constants.NODE_PARAM_NEW_VALUE)

    def unit(self):
        """
        :return: the unit that is used for the value
        """
        return self.json_state.get(api_constants.NODE_PARAM_UNIT)

    def last_update(self):
        """
        :return: the time when this device's value was updated last
        """
        return self.json_state.get(api_constants.NODE_PARAM_UTIME)

    def set_value(self, value):
        """
        Sets a new value for this device.
        This method should be implemented by inheriting classes.

        :param value: the new value to set
        """
        raise NotImplementedError("Not implemented!")

    def update(self):
        """
        Updates the current value of this device.
        This method should be implemented by inheriting classes.
        """
        raise NotImplementedError("Not implemented!")

    def enabled(self):
        """
        :return: Returns if this device is enabled.
        """
        return api_constants.VALUE_DISABLED not in self.json_state[api_constants.NODE_PARAM_TYPE]
