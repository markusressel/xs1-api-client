import json
import unittest
from unittest.mock import MagicMock

from xs1_api_client import api as xs1api


class XS1TestBase(unittest.TestCase):
    _underTest = None

    _test_host = "testhost"

    def setUp(self):
        self._underTest = xs1api.XS1()

        old = self._underTest._send_request

        api_response = XS1TestBase.get_api_response("get_config_info")
        self._underTest._send_request = MagicMock(return_value=api_response)

        self._underTest.set_connection_info(self._test_host)

        self._underTest._send_request = old

    def tearDown(self):
        pass

    @staticmethod
    def get_api_response(filename: str) -> dict:
        """
        Read an api response from a file

        :param filename: the file in the "api_responses" subfolder to read
        :return: the hypothetical api response dict to use as a replacement for the "send_request" method
        """

        import os
        directory = os.path.dirname(__file__)
        file_path = os.path.join(directory, 'api_responses', filename)

        with open(file_path, 'r') as myfile:
            api_response_text = myfile.read()
        return json.loads(api_response_text)

    if __name__ == '__main__':
        unittest.main()
