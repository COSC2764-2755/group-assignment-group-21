import zmq
import os
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("MASTER_PI_PORT", "5050")


def route(action: str, data: dict) -> dict:
    handlers = {
        "ping":            handle_ping,
        "login":           handle_login,
        "register":        handle_register,
        "search_rooms":    handle_search_rooms,
        "book_room":       handle_book_room,
        "cancel_booking":  handle_cancel_booking,
        "checkin":         handle_checkin,
        "checkout":        handle_checkout,
        "validate_token":  handle_validate_token,
        "report_fault":    handle_report_fault,
        "update_status":   handle_update_status,
        "save_sensor":     handle_save_sensor,
        "get_room_info":   handle_get_room_info,
        "get_bookings":    handle_get_bookings,
    }
    handler = handlers.get(action)
    if handler is None:
        return {"status": "error", "message": f"Unknown action: {action}"}
    return handler(data)


# ── handlers ──────────────────────────────────────────

def handle_ping(data):
    return {"status": "ok", "message": "pong"}


def handle_login(data):
    # expects: university_id, password
    # TODO: query DB, verify bcrypt hash, return role
    return {
        "status": "ok",
        "user_id": 1,
        "full_name": "Alice Johnson",
        "role": "user"
    }


def handle_register(data):
    # expects: university_id, full_name, email, password
    # TODO: hash password, insert into users table
    return {"status": "ok", "message": "Registered successfully"}


def handle_search_rooms(data):
    # expects: date, start_time, end_time
    # TODO: query rooms not booked in that slot
    return {
        "status": "ok",
        "rooms": [
            {"id": 1, "room_code": "A201", "building": "Building A", "capacity": 30, "status": "available"},
            {"id": 2, "room_code": "B101", "building": "Building B", "capacity": 40, "status": "available"},
        ]
    }


def handle_book_room(data):
    # expects: user_id, room_id, date, start_time, end_time
    # TODO: insert booking, generate token, insert token
    return {
        "status": "ok",
        "booking_id": 1,
        "token": "tok_a1b2c3d4e5f6"
    }


def handle_cancel_booking(data):
    # expects: booking_id, user_id
    # TODO: update booking status to cancelled
    return {"status": "ok", "message": "Booking cancelled"}


def handle_checkin(data):
    # expects: booking_id, user_id
    # TODO: update room status to in_use, log action
    return {"status": "ok", "message": "Checked in successfully"}


def handle_checkout(data):
    # expects: booking_id, user_id
    # TODO: update room status to available, log action
    return {"status": "ok", "message": "Checked out successfully"}


def handle_validate_token(data):
    # expects: token, room_id
    # TODO: check token exists, unused, matches room, mark used
    return {
        "status": "ok",
        "user": "Alice Johnson",
        "booking_id": 1,
        "end_time": "12:00"
    }


def handle_report_fault(data):
    # expects: room_id, user_id (nullable), description
    # TODO: insert into fault_reports, update room status to fault
    return {"status": "ok", "message": "Fault reported successfully"}


def handle_update_status(data):
    # expects: room_id, new_status, changed_by
    # TODO: update room status, insert into room_status_log
    return {"status": "ok", "message": "Room status updated"}


def handle_save_sensor(data):
    # expects: room_id, temperature, humidity, pressure
    # TODO: insert into sensor_readings
    return {"status": "ok", "message": "Sensor data saved"}


def handle_get_room_info(data):
    # expects: room_id
    # TODO: query room status, next booking, latest sensor reading
    return {
        "status": "ok",
        "room": {
            "id": 1,
            "room_code": "A201",
            "building": "Building A",
            "capacity": 30,
            "status": "available"
        },
        "next_booking": {
            "start_time": "10:00",
            "end_time": "12:00",
            "user": "Alice Johnson"
        },
        "sensor": {
            "temperature": 22.5,
            "humidity": 55.3,
            "pressure": 1013.2
        }
    }


def handle_get_bookings(data):
    # expects: user_id
    # TODO: query bookings for this user
    return {
        "status": "ok",
        "bookings": [
            {
                "id": 1,
                "room_code": "A201",
                "date": "2026-05-01",
                "start_time": "10:00",
                "end_time": "12:00",
                "status": "active",
                "token": "tok_a1b2c3d4e5f6"
            }
        ]
    }

def start():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://0.0.0.0:{PORT}")
    print(f"[SERVER] Listening on port {PORT}...")

    while True:
        payload = socket.recv_json()
        print(f"[SERVER] Received: {payload}")

        action = payload.get("action")
        data = payload.get("data", {})

        response = route(action, data)

        print(f"[SERVER] Sending: {response}")
        socket.send_json(response)


