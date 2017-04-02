import unittest

from xs1_api_client import api as xs1api


class TestXS1(unittest.TestCase):
    def test_create_api(self):
        host = "192.168.2.75"

        api = xs1api.XS1(host)

        self.assertIsNotNone(api)


if __name__ == '__main__':
    unittest.main()
