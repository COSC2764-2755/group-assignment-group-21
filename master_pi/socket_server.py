import zmq
import os
import hashlib
import re
from dotenv import load_dotenv
from mqtt_publisher import publish_message
from db import get_connection

load_dotenv()

PORT = os.getenv("MASTER_PI_PORT", "5050")


def route(action: str, data: dict) -> dict:
    handlers = {
        "ping": handle_ping,
        "login": handle_login,
        "register": handle_register,
        "search_rooms": handle_search_rooms,
        "book_room": handle_book_room,
        "cancel_booking": handle_cancel_booking,
        "checkin": handle_checkin,
        "checkout": handle_checkout,
        "validate_token": handle_validate_token,
        "report_fault": handle_report_fault,
        "update_status": handle_update_status,
        "save_sensor": handle_save_sensor,
        "get_room_info": handle_get_room_info,
        "get_bookings": handle_get_bookings,
    }

    handler = handlers.get(action)

    if handler is None:
        return {
            "status": "error",
            "message": f"Unknown action: {action}"
        }

    return handler(data)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def hash_password(password: str) -> str:
    """SHA-256 hash of the password."""
    return hashlib.sha256(password.encode()).hexdigest()


def is_valid_email(email: str) -> bool:
    """Basic email format check."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None


def log_action(conn, user_id, action, detail=""):
    """Insert a row into action_logs."""
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO action_logs (user_id, action, detail) VALUES (%s, %s, %s)",
            (user_id, action, detail)
        )
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"[LOG ERROR] {e}")


# --------------------------------------------------
# HANDLERS
# --------------------------------------------------

def handle_ping(data):
    return {
        "status": "ok",
        "message": "pong"
    }


def handle_login(data):
    return {
        "status": "ok",
        "user_id": 1,
        "full_name": "Alice Johnson",
        "role": "user"
    }


def handle_register(data):
    """
    Validates input, checks for duplicates, hashes password,
    and inserts a new user into the database.

    Expected data keys:
        university_id, full_name, email, password
    """
    university_id = data.get("university_id", "").strip()
    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # ── Input validation ──────────────────────────────
    if not all([university_id, full_name, email, password]):
        return {
            "status": "error",
            "message": "All fields are required."
        }

    if not is_valid_email(email):
        return {
            "status": "error",
            "message": "Invalid email address format."
        }

    if len(password) < 8:
        return {
            "status": "error",
            "message": "Password must be at least 8 characters."
        }

    # ── Database operations ───────────────────────────
    conn = get_connection()
    if conn is None:
        return {
            "status": "error",
            "message": "Database connection failed."
        }

    try:
        cursor = conn.cursor(dictionary=True)

        # Check for duplicate university_id or email
        cursor.execute(
            "SELECT id FROM users WHERE university_id = %s OR email = %s",
            (university_id, email)
        )
        existing = cursor.fetchone()

        if existing:
            return {
                "status": "error",
                "message": "University ID or email is already registered."
            }

        # Insert the new user
        password_hash = hash_password(password)
        cursor.execute(
            """INSERT INTO users (university_id, full_name, email, password_hash, role)
               VALUES (%s, %s, %s, %s, 'user')""",
            (university_id, full_name, email, password_hash)
        )
        conn.commit()
        new_user_id = cursor.lastrowid
        cursor.close()

        # Log the registration action
        log_action(conn, new_user_id, "register", f"New user registered: {university_id}")

        print(f"[REGISTER] New user registered: {university_id} ({email})")

        return {
            "status": "ok",
            "message": "Registered successfully."
        }

    except Exception as e:
        print(f"[REGISTER ERROR] {e}")
        return {
            "status": "error",
            "message": "Registration failed due to a server error."
        }

    finally:
        conn.close()


def handle_search_rooms(data):
    return {
        "status": "ok",
        "rooms": [
            {
                "id": 1,
                "room_code": "A201",
                "building": "Building A",
                "capacity": 30,
                "status": "available"
            },
            {
                "id": 2,
                "room_code": "B101",
                "building": "Building B",
                "capacity": 40,
                "status": "available"
            }
        ]
    }


def handle_book_room(data):
    return {
        "status": "ok",
        "booking_id": 1,
        "token": "tok_a1b2c3d4e5f6"
    }


def handle_cancel_booking(data):
    return {
        "status": "ok",
        "message": "Booking cancelled"
    }


def handle_checkin(data):
    publish_message(
        "room/1/status",
        "in_use"
    )

    return {
        "status": "ok",
        "message": "Checked in successfully"
    }


def handle_checkout(data):
    publish_message(
        "room/1/status",
        "available"
    )

    return {
        "status": "ok",
        "message": "Checked out successfully"
    }


def handle_validate_token(data):
    token = data.get("token")
    room_id = data.get("room_id")

    # Later teammate can replace this with DB validation
    if token == "tok_a1b2c3d4e5f6":

        publish_message(
            f"room/{room_id}/status",
            "in_use"
        )

        return {
            "status": "ok",
            "user": "Alice Johnson",
            "booking_id": 1,
            "end_time": "12:00",
            "message": "Access granted"
        }

    return {
        "status": "failed",
        "message": "Invalid token"
    }


def handle_report_fault(data):
    room_id = data.get("room_id")

    publish_message(
        f"room/{room_id}/status",
        "fault"
    )

    publish_message(
        "security/alerts",
        f"Room {room_id} entered FAULT status"
    )

    return {
        "status": "ok",
        "message": "Fault reported successfully"
    }


def handle_update_status(data):
    room_id = data.get("room_id")
    new_status = data.get("new_status")

    publish_message(
        f"room/{room_id}/status",
        new_status
    )

    return {
        "status": "ok",
        "message": "Room status updated"
    }


def handle_save_sensor(data):
    return {
        "status": "ok",
        "message": "Sensor data saved"
    }


def handle_get_room_info(data):
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


# --------------------------------------------------
# START SERVER
# --------------------------------------------------

def start():
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    socket.bind(f"tcp://0.0.0.0:{PORT}")

    print(f"[MASTER PI SERVER] Listening on port {PORT}...")

    while True:
        payload = socket.recv_json()

        print(f"[SERVER] Received: {payload}")

        action = payload.get("action")
        data = payload.get("data", {})

        response = route(action, data)

        print(f"[SERVER] Sending: {response}")

        socket.send_json(response)


if __name__ == "__main__":
    start()
