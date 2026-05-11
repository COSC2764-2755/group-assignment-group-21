import unittest
from master_pi.socket_server import handle_login


class TestAuthentication(unittest.TestCase):

    def test_login_success(self):
        data = {
            "university_id": "s123456",
            "password": "password123"
        }

        response = handle_login(data)

        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["role"], "user")

    def test_login_response_contains_name(self):
        data = {
            "university_id": "s123456",
            "password": "password123"
        }

        response = handle_login(data)

        self.assertIn("full_name", response)


if __name__ == "__main__":
    unittest.main()