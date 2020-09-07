from tests import XS1TestBase
from xs1_api_client import api as xs1api
from xs1_api_client.api_constants import ActuatorType


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
