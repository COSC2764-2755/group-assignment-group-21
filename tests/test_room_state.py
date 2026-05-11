import unittest
from master_pi.socket_server import handle_report_fault


class TestRoomState(unittest.TestCase):

    def test_fault_status_update(self):
        data = {
            "room_id": 1,
            "description": "Projector broken"
        }

        response = handle_report_fault(data)

        self.assertEqual(response["status"], "ok")
        self.assertEqual(
            response["message"],
            "Fault reported successfully"
        )


if __name__ == "__main__":
    unittest.main()