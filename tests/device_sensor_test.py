from unittest.mock import MagicMock

from tests import XS1TestBase
from xs1_api_client.api_constants import UrlParam


class TestXS1(XS1TestBase):
    def test_api_get_all_sensors(self):
        api_response = TestXS1.get_api_response("get_list_sensors")
        self._underTest._send_request = MagicMock(return_value=api_response)

        sensors = self._underTest.get_all_sensors()
        self.assertIsNotNone(sensors)

    def test_api_get_specific_sensor(self):
        api_response = TestXS1.get_api_response("get_list_sensors")
        self._underTest._send_request = MagicMock(return_value=api_response)

        sensor_2 = self._underTest.get_sensor(2)
        self.assertIsNotNone(sensor_2)

    def test_api_get_config_sensor(self):
        api_response = TestXS1.get_api_response("get_config_sensor")
        self._underTest._send_request = MagicMock(return_value=api_response)

        config = self._underTest.get_config_sensor(2)
        self.assertIsNotNone(config)

    def test_api_set_config_sensor(self):
        api_response = TestXS1.get_api_response("set_config_sensor")
        self._underTest._send_request = MagicMock(return_value=api_response)

        new_config = {UrlParam.NAME: "Keller_",
                      UrlParam.SYSTEM: "ws300",
                      UrlParam.TYPE: "hygrometer",
                      UrlParam.HC1: 0,
                      UrlParam.HC2: 0,
                      UrlParam.ADDRESS: 3,
                      UrlParam.FACTOR: 1.000000,
                      UrlParam.OFFSET: 0.000000,
                      UrlParam.X: 0,
                      UrlParam.Y: 0,
                      UrlParam.Z: 0,
                      UrlParam.LOG: "off"
                      }

        response = self._underTest.set_config_sensor(2, new_config)
        self.assertIsNotNone(response)

    def test_api_get_state_sensor(self):
        api_response = TestXS1.get_api_response("get_state_sensor")
        self._underTest._send_request = MagicMock(return_value=api_response)

        response = self._underTest.get_state_sensor(1)
        self.assertIsNotNone(response)
