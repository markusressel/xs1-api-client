from xs1_api_client import api_constants
from ..base import XS1Device


class XS1Actuator(XS1Device):
    """
    Represents a basic XS1 Actuator, there may be special variants for some types.
    """

    def __init__(self, state, api_interface):
        super(XS1Actuator, self).__init__(state, api_interface)

    def update(self):
        """
        Updates the state of this actuator
        """
        state = self.api_interface.get_state_actuator(self.id())
        self.set_state(state)

    def set_value(self, value):
        """
        Sets a new value for this actuator

        :param value: new value to set
        """
        new_state = self.api_interface.set_actuator_value(self.id(), value)
        self.set_state(new_state)

    def get_functions(self):
        """
        :return: a list of functions that can be executed using the call_function() method
        """
        functions = []
        for idx, function in enumerate(self._state[api_constants.NODE_PARAM_FUNCTION]):
            if function[api_constants.NODE_PARAM_TYPE] is not api_constants.VALUE_DISABLED:
                functions.append(XS1Function(self, idx + 1, function[api_constants.NODE_PARAM_TYPE],
                                             function[api_constants.NODE_PARAM_DESCRIPTION]))

        return functions

    def call_function(self, function):
        """
        Calls the specified function by id and saves the api response as the new state

        :param function: XS1Function object
        """
        if not isinstance(function, XS1Function):
            raise ValueError('Invalid function object type! Has to be a XS1Function!')

        self.api_interface.call_actuator_function(self, function.id())


class XS1Function(object):
    """
    Represents a function of a XS1Actuator.
    """

    def __init__(self, actuator, id, type, description):
        """
        Creates a function object

        :param actuator: the actuator this function belongs to
        :param id: the id of this function
        :param type: the type of this function (as a string)
        :param description: a description for this function
        """
        self._actuator = actuator
        self._id = id
        self._type = type
        self._description = description

    def id(self):
        """
        :return: the id of this function (note that this id is only unique for a single actuator!)
        """
        return self._id

    def type(self):
        """
        :return: the type of this function
        """
        return self._type

    def description(self):
        """
        :return: a description for this function
        """
        return self._description

    def execute(self):
        """
        Executes this function and sets the response as the new actuator value
        """
        self._actuator.api_interface.call_actuator_function(self._actuator, self._id)
