import unittest

from xs1_api_client import api as xs1api


class TestXS1(unittest.TestCase):
    def test_api(self):
        self.assertIsNotNone(xs1api)


if __name__ == '__main__':
    unittest.main()
