from unittest.mock import MagicMock

from tests import XS1TestBase
from xs1_api_client.api_constants import Node, UrlParam, FunctionType, ActuatorType


class TestXS1(XS1TestBase):
    def test_api_get_all_actuators(self):
        api_response = TestXS1.get_api_response("get_list_actuators")
        self._underTest._send_request = MagicMock(return_value=api_response)

        actuators = self._underTest.get_all_actuators()
        self.assertIsNotNone(actuators)

        for actuator in actuators:
            if actuator.type() == ActuatorType.SWITCH:
                from xs1_api_client.device.actuator.switch import XS1Switch
                self.assertTrue(isinstance(actuator, XS1Switch))
            if actuator.type() == ActuatorType.TEMPERATURE:
                from xs1_api_client.device.actuator.thermostat import XS1Thermostat
                self.assertTrue(isinstance(actuator, XS1Thermostat))

    def test_api_get_specific_actuator(self):
        api_response = TestXS1.get_api_response("get_list_actuators")
        self._underTest._send_request = MagicMock(return_value=api_response)

        actuator_1 = self._underTest.get_actuator(1)
        self.assertIsNotNone(actuator_1)

    def test_api_get_config_actuator(self):
        api_response = TestXS1.get_api_response("get_config_actuator")
        self._underTest._send_request = MagicMock(return_value=api_response)

        config = self._underTest.get_config_actuator(1)
        self.assertIsNotNone(config)

    def test_api_set_config_actuator(self):
        api_response = TestXS1.get_api_response("set_config_actuator")
        self._underTest._send_request = MagicMock(return_value=api_response)

        new_config = {UrlParam.NAME: "Fernsehlampe",
                      UrlParam.SYSTEM: "ab400",
                      UrlParam.TYPE: "switch",
                      UrlParam.HC1: 26,
                      UrlParam.HC2: 0,
                      UrlParam.ADDRESS: 1,
                      UrlParam.FUNCTION: [
                          {Node.PARAM_TYPE: FunctionType.ON, Node.PARAM_DESCRIPTION: "ON"},
                          {UrlParam.TYPE: FunctionType.OFF, "dsc": "OFF"},
                          {UrlParam.TYPE: FunctionType.DISABLED, "dsc": ""},
                          {UrlParam.TYPE: FunctionType.DISABLED, "dsc": ""}
                      ],
                      UrlParam.X: 0,
                      UrlParam.Y: 0,
                      UrlParam.Z: 0,
                      UrlParam.LOG: "off"
                      }

        response = self._underTest.set_config_actuator(1, new_config)
        self.assertIsNotNone(response)

    def test_api_get_state_actuator(self):
        api_response = TestXS1.get_api_response("get_state_actuator")
        self._underTest._send_request = MagicMock(return_value=api_response)

        response = self._underTest.get_state_actuator(1)
        self.assertIsNotNone(response)

    def test_api_call_actuator_function(self):
        api_response = TestXS1.get_api_response("call_actuator_function")
        self._underTest._send_request = MagicMock(return_value=api_response)

        response = self._underTest.call_actuator_function(1, FunctionType.OFF)
        self.assertEqual(response[Node.ACTUATOR.value][Node.PARAM_VALUE.value], 0)
        self.assertIsNotNone(response)

    def test_api_update_specific_actuator(self):
        api_response = TestXS1.get_api_response("get_list_actuators")
        self._underTest._send_request = MagicMock(return_value=api_response)

        actuator_1 = self._underTest.get_actuator(1)
        self.assertEqual(actuator_1.value(), 0.0)
        self.assertEqual(actuator_1.new_value(), 0.0)

        api_response = TestXS1.get_api_response("get_state_actuator__updated")
        self._underTest._send_request = MagicMock(return_value=api_response)

        actuator_1.update()

        self.assertEqual(actuator_1.value(), 16.0)
        self.assertEqual(actuator_1.new_value(), 18.0)
