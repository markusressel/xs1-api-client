from unittest.mock import MagicMock

from tests import XS1TestBase


class TestXS1(XS1TestBase):
    def test_config_info(self):
        """
        Tests the retrieval of the xs1 config info (that cant be edited)
        """

        test_host = "192.168.2.1"
        test_user = "User"
        test_password = "Password"

        api_response = TestXS1.get_api_response("get_config_info")
        self._underTest._send_request = MagicMock(return_value=api_response)

        self._underTest.set_connection_info(host=test_host, user=test_user, password=test_password)

        self.assertEqual(self._underTest.get_host(), test_host)
        self.assertEqual(self._underTest.get_user(), test_user)
        self.assertEqual(self._underTest.get_password(), test_password)

        self.assertEqual(self._underTest.get_gateway_name(), "xs1")
        self.assertEqual(self._underTest.get_gateway_bootloader_version(), "1.0.0.6")
        self.assertEqual(self._underTest.get_gateway_firmware_version(), "4.0.0.5326")
        self.assertEqual(self._underTest.get_gateway_hardware_version(), "1.3.0.1BB")
        self.assertEqual(self._underTest.get_gateway_mac(), "00:1B:C5:01:D9:B3")
        self.assertEqual(self._underTest.get_gateway_uptime(), 963766)

    def test_main_config(self):
        """
        Tests the retrieval of the xs1 config info (that cant be edited)
        """

        api_response = TestXS1.get_api_response("get_config_main")
        self._underTest._send_request = MagicMock(return_value=api_response)

        main_config = self._underTest.get_config_main()

        self.assertIsNotNone(main_config)

    def test_api_constants_functions(self):
        """
        Tests if there is an ApiConstant for every supported function type
        """

        api_response = TestXS1.get_api_response("get_list_functions")
        self._underTest._send_request = MagicMock(return_value=api_response)

        from xs1_api_client.api_constants import FunctionType

        for fun in self._underTest.get_list_functions():
            function_type = FunctionType(fun['name'])
            self.assertIsNotNone(function_type)

    def test_api_constants_systems(self):
        """
        Tests if there is an ApiConstant for every supported System type
        """

        api_response = TestXS1.get_api_response("get_list_systems")
        self._underTest._send_request = MagicMock(return_value=api_response)

        from xs1_api_client.api_constants import SystemType

        for system in self._underTest.get_list_systems():
            system_type = SystemType(system['name'])
            self.assertIsNotNone(system_type)

    def test_api_constants_actuator_types(self):
        """
        Tests if there is an ApiConstant for every supported actuator type
        """

        api_response = TestXS1.get_api_response("get_types_actuators")
        self._underTest._send_request = MagicMock(return_value=api_response)

        from xs1_api_client.api_constants import ActuatorType

        for t in self._underTest.get_types_actuators():
            actuator_type = ActuatorType(t['name'])
            self.assertIsNotNone(actuator_type)

    def test_api_constants_sensor_types(self):
        """
        Tests if there is an ApiConstant for every supported actuator type
        """

        api_response = TestXS1.get_api_response("get_types_sensors")
        self._underTest._send_request = MagicMock(return_value=api_response)

        from xs1_api_client.api_constants import SensorType

        for t in self._underTest.get_types_sensors():
            sensor_type = SensorType(t['name'])
            self.assertIsNotNone(sensor_type)
