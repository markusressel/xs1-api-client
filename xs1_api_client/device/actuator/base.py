from xs1_api_client import api_constants, XS1
from ..base import XS1Device


class XS1Actuator(XS1Device):
    """
    Represents a basic XS1 Actuator, there may be special variants for some types.
    """

    def __init__(self, state, api: XS1):
        super(XS1Actuator, self).__init__(state, api)

    def update(self) -> None:
        """
        Updates the state of this actuator
        """
        response = self._api_interface.get_state_actuator(self.id())
        self.set_state(response[api_constants.NODE_ACTUATOR])

    def set_value(self, value) -> None:
        """
        Sets a new value for this actuator

        :param value: new value to set
        """
        new_state = self._api_interface.set_actuator_value(self.id(), value)
        self.set_state(new_state[api_constants.NODE_ACTUATOR])

    def get_functions(self) -> [XS1Function]:
        """
        :return: a list of functions that can be executed using the call_function() method
        """
        functions = []
        for idx, xs1_function in enumerate(self._state[api_constants.NODE_PARAM_FUNCTION]):
            if xs1_function[api_constants.NODE_PARAM_TYPE] is not api_constants.VALUE_DISABLED:
                functions.append(XS1Function(self, idx + 1, xs1_function[api_constants.NODE_PARAM_TYPE],
                                             xs1_function[api_constants.NODE_PARAM_DESCRIPTION]))

        return functions

    def call_function(self, xs1_function: XS1Function):
        """
        Calls the specified function by id and saves the api response as the new state

        :param xs1_function: XS1Function object
        """
        if not isinstance(xs1_function, XS1Function):
            raise ValueError('Invalid function object type! Has to be a XS1Function!')

        response = self._api_interface.call_actuator_function(self.id(), xs1_function.id())
        self.set_state(response[api_constants.NODE_ACTUATOR])


class XS1Function(object):
    """
    Represents a function of a XS1Actuator.
    """

    def __init__(self, actuator: XS1Actuator, function_id: str, function_type: str, description: str):
        """
        Creates a function object

        :param actuator: the actuator this function belongs to
        :param function_id: the id of this function
        :param function_type: the type of this function (as a string)
        :param description: a description for this function
        """
        self._actuator = actuator
        self._id = function_id
        self._type = function_type
        self._description = description

    def id(self) -> str:
        """
        :return: the id of this function (note that this id is only unique for a single actuator!)
        """
        return self._id

    def type(self) -> str:
        """
        :return: the type of this function
        """
        return self._type

    def description(self) -> str:
        """
        :return: a description for this function
        """
        return self._description

    def execute(self) -> None:
        """
        Executes this function and sets the response as the new actuator value
        """
        self._actuator.call_function(self)
