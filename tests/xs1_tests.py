from unittest.mock import MagicMock

from tests import XS1TestBase


class TestXS1(XS1TestBase):
    def test_config_info(self):
        """
        Tests if a basic import and class instantiation works
        """

        test_host = "192.168.2.1"
        test_user = "User"
        test_password = "Password"

        api_response = TestXS1.get_api_response("get_config_info")
        self._underTest._send_request = MagicMock(return_value=api_response)

        self._underTest.set_connection_info(test_host, test_user, test_password)

        self.assertEqual(self._underTest.get_gateway_name(), "xs1")
        self.assertEqual(self._underTest.get_gateway_bootloader_version(), "1.0.0.6")
        self.assertEqual(self._underTest.get_gateway_firmware_version(), "4.0.0.5326")
        self.assertEqual(self._underTest.get_gateway_hardware_version(), "1.3.0.1BB")
        self.assertEqual(self._underTest.get_gateway_mac(), "00:1B:C5:01:D9:B3")
        self.assertEqual(self._underTest.get_gateway_uptime(), 963766)
