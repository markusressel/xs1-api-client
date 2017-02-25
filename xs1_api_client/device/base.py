from .. import api_constants


class XS1Device(object):
    """
    This is a generic XS1 device, all other objetcs inherit from this.
    """

    def __init__(self, state: dict, api_interface):
        """
        Initializes the device.

        :param state: json representation of this device (api response)
        :param api_interface: the interface for handling api requests like fetching and setting values
        """
        self.api_interface = api_interface
        self._state = state

    def set_state(self, new_state: dict):
        """
        Sets a new state for this device.
        If there is an existing state, new and old values will be merged
        to retain any information that was missing from api responses.

        :param new_state: new representation of this device (api response)
        """
        if self._state:
            for key, value in new_state.items():
                self._state[key] = value

            #  self._state = {**self._state, **new_state}  # merge dicts (Python 3.5 required)
        else:
            self._state = new_state  # set initial state

    def id(self):
        """
        :return: id of this device
        """
        device_id = self._state.get(api_constants.NODE_PARAM_NUMBER)
        if device_id is None:
            device_id = self._state.get(api_constants.NODE_PARAM_ID)
        return device_id

    def type(self):
        """
        :return: the type of this device
        """
        return self._state.get(api_constants.NODE_PARAM_TYPE)

    def name(self):
        """
        :return: the name of this device
        """
        return self._state.get(api_constants.NODE_PARAM_NAME)

    def value(self):
        """
        :return: the current value of this device
        """
        return self._state.get(api_constants.NODE_PARAM_VALUE)

    def new_value(self):
        """
        Returns the new value to set for this device.
        If this value differs from the currrent value the gateway is still trying to update the value on the device.
        If it does not differ the value has already been set.

        :return: the new value to set for this device
        """
        return self._state.get(api_constants.NODE_PARAM_NEW_VALUE)

    def unit(self):
        """
        :return: the unit that is used for the value
        """
        return self._state.get(api_constants.NODE_PARAM_UNIT)

    def last_update(self):
        """
        :return: the time when this device's value was updated last
        """
        return self._state.get(api_constants.NODE_PARAM_UTIME)

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
        return api_constants.VALUE_DISABLED not in self._state[api_constants.NODE_PARAM_TYPE]
