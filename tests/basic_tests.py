from unittest.mock import MagicMock

from tests import XS1TestBase
from xs1_api_client import api as xs1api
from xs1_api_client.api_constants import ActuatorType, FunctionType, SystemType


class TestXS1(XS1TestBase):
    def test_device(self):
        """
        Tests if a basic import and class instantiation works
        """
        self.assertIsNotNone(xs1api)
        self.assertIsNotNone(self._underTest)

    def test_api_constants_equals(self):
        """
        Tests the "equals" method of ApiConstants
        """

        self.assertNotEqual(ActuatorType.DIMMER, ActuatorType.DISABLED)
        self.assertNotEqual(ActuatorType.DIMMER, ActuatorType.DISABLED.name)
        self.assertNotEqual(ActuatorType.DIMMER, "disabled")
        self.assertNotEqual(ActuatorType.DIMMER, ActuatorType.DIMMER.name)

        self.assertEqual(ActuatorType.DIMMER, ActuatorType.DIMMER)
        self.assertEqual(ActuatorType.DIMMER, ActuatorType.DIMMER.value)
        self.assertEqual(ActuatorType.DIMMER, "dimmer")
        self.assertEqual(ActuatorType.DIMMER, 'dimmer')

        self.assertTrue(ActuatorType.DISABLED in ["disabled"])

    def test_api_constants_functions(self):
        """
        Tests if there is an ApiConstant for every supported function type
        """

        api_response = TestXS1.get_api_response("get_list_functions")
        self._underTest._send_request = MagicMock(return_value=api_response)

        for fun in self._underTest.get_list_functions():
            function_type = FunctionType(fun['name'])
            self.assertIsNotNone(function_type)

    def test_api_constants_systems(self):
        """
        Tests if there is an ApiConstant for every supported System type
        """

        api_response = TestXS1.get_api_response("get_list_systems")
        self._underTest._send_request = MagicMock(return_value=api_response)

        for system in self._underTest.get_list_systems():
            system_type = SystemType(system['name'])
            self.assertIsNotNone(system_type)
