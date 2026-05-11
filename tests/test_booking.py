import unittest
from master_pi.socket_server import handle_book_room


class TestBooking(unittest.TestCase):

    def test_booking_success(self):
        data = {
            "user_id": 1,
            "room_id": 1,
            "date": "2026-05-10",
            "start_time": "10:00",
            "end_time": "12:00"
        }

        response = handle_book_room(data)

        self.assertEqual(response["status"], "ok")
        self.assertIn("token", response)


if __name__ == "__main__":
    unittest.main()