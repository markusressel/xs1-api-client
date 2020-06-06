from xs1_api_client.api_constants import Node, FunctionType
from xs1_api_client.device import XS1Device


class XS1Actuator(XS1Device):
    """
    Represents a basic XS1 Actuator, there may be special variants for some types.
    """

    def __init__(self, state, api):
        super(XS1Actuator, self).__init__(state, api)

    def __str__(self):
        return "Actuator: " + super(XS1Actuator, self).__str__()

    def update(self) -> None:
        """
        Updates the state of this actuator
        """
        response = self._api_interface.get_state_actuator(self.number())
        new_value = self._get_node_value(response, Node.ACTUATOR)
        self.set_state(new_value)

    def set_name(self, name: str):
        """
        Sets a new name for this device.
        Keep in mind that there are some limitations for a device name.
        :param name: the new name to set
        :return: the new name of the actuator
        """
        # check name arg for validity
        super(XS1Actuator, self).set_name(name)

        config = self._api_interface.get_config_actuator(self.number())

        # name is already set, to minimize flash writes don't write it again
        if config["name"] == name:
            return name

        config["name"] = name

        result = self._api_interface.set_config_actuator(self.number(), config)
        new_name = self._get_node_value(result, "name")

        # save new_name to internal state
        self._state[Node.PARAM_NAME.value] = new_name

        return new_name

    def set_value(self, value) -> None:
        """
        Sets a new value for this actuator
        :param value: new value to set
        """
        new_state = self._api_interface.set_actuator_value(self.number(), value)
        new_value = self._get_node_value(new_state, Node.ACTUATOR)
        self.set_state(new_value)

    def get_function_by_id(self, func_id):
        """
        Get a function by it's id
        :param func_id: function id
        :return: XS1Function or None
        """
        for xs1_function in self.get_functions():
            if xs1_function.id() == func_id:
                return xs1_function

        return None

    def get_function_by_type(self, func_type: FunctionType):
        """
        Get a function by it's type
        :param func_type: function type
        :return: XS1Function or None
        """
        for xs1_function in self.get_functions():
            if xs1_function.type() == func_type:
                return xs1_function

        return None

    def get_functions(self) -> []:
        """
        :return: a list of functions that can be executed using the call_function() method
        """
        functions = []
        for idx, xs1_function in enumerate(self._get_node_value(self._state, Node.PARAM_FUNCTION)):
            if self._get_node_value(xs1_function, Node.PARAM_TYPE) != FunctionType.DISABLED.value:
                try:
                    function_type = FunctionType(self._get_node_value(xs1_function, Node.PARAM_TYPE))
                except ValueError:
                    function_type = FunctionType.UNKNOWN

                functions.append(
                    XS1Function(self,
                                idx + 1,
                                function_type,
                                self._get_node_value(xs1_function, Node.PARAM_DESCRIPTION)
                                )
                )

        return functions

    def call_function(self, xs1_function):
        """
        Calls the specified function by id and saves the api response as the new state
        :param xs1_function: XS1Function object
        """
        if not isinstance(xs1_function, XS1Function):
            raise ValueError('Invalid function object type! Has to be a XS1Function!')

        response = self._api_interface.call_actuator_function(self.id(), xs1_function.id())
        new_value = self._get_node_value(response, Node.ACTUATOR)
        self.set_state(new_value)


class XS1Function(object):
    """
    Represents a function of a XS1Actuator.
    """

    def __init__(self, actuator: XS1Actuator, function_id: int, function_type: FunctionType, description: str):
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

    def __str__(self):
        return "Function: %s (ID: %i, Type: %s, Description: %s)" % (
            self.description(), self.id(), self.type(), self.description())

    def id(self) -> int:
        """
        :return: the id of this function (note that this id is only unique for a single actuator!)
        """
        return self._id

    def type(self) -> FunctionType:
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
