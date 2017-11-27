import json
import unittest

from xs1_api_client import api as xs1api


class XS1TestBase(unittest.TestCase):
    _underTest = None

    def setUp(self):
        self._underTest = xs1api.XS1()

    def tearDown(self):
        pass

    @staticmethod
    def get_api_response(filename: str) -> dict:
        """
        Read an api response from a file

        :param filename: the file in the "api_responses" subfolder to read
        :return: the hypothetical api response dict to use as a replacement for the "send_request" method
        """

        with open('api_responses/%s' % filename, 'r') as myfile:
            api_response_text = myfile.read()
        return json.loads(api_response_text)

    if __name__ == '__main__':
        unittest.main()
