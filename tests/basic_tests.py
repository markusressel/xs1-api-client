import unittest

from xs1_api_client import api as xs1api
from xs1_api_client.api_constants import ActuatorType


class TestXS1(unittest.TestCase):
    def test_api(self):
        self.assertIsNotNone(xs1api)

    def test_api_constants(self):
        self.assertNotEquals(ActuatorType.DIMMER, ActuatorType.DISABLED)
        self.assertNotEquals(ActuatorType.DIMMER, ActuatorType.DISABLED.name)
        self.assertNotEquals(ActuatorType.DIMMER, "disabled")
        self.assertNotEquals(ActuatorType.DIMMER, ActuatorType.DIMMER.name)

        self.assertEquals(ActuatorType.DIMMER, ActuatorType.DIMMER)
        self.assertEquals(ActuatorType.DIMMER, ActuatorType.DIMMER.value)
        self.assertEquals(ActuatorType.DIMMER, "dimmer")
        self.assertEquals(ActuatorType.DIMMER, 'dimmer')

        self.assertTrue(ActuatorType.DISABLED in ["disabled"])


if __name__ == '__main__':
    unittest.main()
