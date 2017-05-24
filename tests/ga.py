import unittest
import mock
from googleapiclient import _auth


class TestAuthWithGoogleAuth(unittest.TestCase):
    def setUp(self):
        _auth.HAS_GOOGLE_AUTH = True
        _auth.HAS_OAUTH2CLIENT = False

    def tearDown(self):
        _auth.HAS_GOOGLE_AUTH = True
        _auth.HAS_OAUTH2CLIENT = True

    def test_default_credentials(self):
        with mock.patch('google.auth.default', autospec=True) as default:
            default.return_value = (
                mock.sentinel.credentials, mock.sentinel.project)

            credentials = _auth.default_credentials()

            self.assertEqual(credentials, mock.sentinel.credentials)


class TestAuthWithoutAuth(unittest.TestCase):

    def setUp(self):
        _auth.HAS_GOOGLE_AUTH = False
        _auth.HAS_OAUTH2CLIENT = False

    def tearDown(self):
        _auth.HAS_GOOGLE_AUTH = True
        _auth.HAS_OAUTH2CLIENT = True

    def test_default_credentials(self):
        with self.assertRaises(EnvironmentError):
            print(_auth.default_credentials())


if __name__ == '__main__':
    unittest.main()