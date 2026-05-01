from socket_client import ping, register, login, search_rooms, book_room, get_bookings, checkin, validate_token, checkout, cancel_booking, report_fault, update_room_status

# ── test all actions ───────────────────────────────────

if __name__ == "__main__":
    print("\n── ping ──")
    print(ping())

    print("\n── register ──")
    print(register("S001", "Alice Johnson", "alice@uni.edu.au", "password123"))

    print("\n── login ──")
    print(login("S001", "password123"))

    print("\n── search rooms ──")
    print(search_rooms("2026-05-10", "10:00", "12:00"))

    print("\n── book room ──")
    print(book_room(1, 1, "2026-05-10", "10:00", "12:00"))

    print("\n── get bookings ──")
    print(get_bookings(1))

    print("\n── checkin ──")
    print(checkin(1, 1))

    print("\n── validate token ──")
    print(validate_token("tok_a1b2c3d4e5f6", 1))

    print("\n── checkout ──")
    print(checkout(1, 1))

    print("\n── cancel booking ──")
    print(cancel_booking(1, 1))

    print("\n── report fault ──")
    print(report_fault(1, 1, "Projector not working"))

    print("\n── update room status ──")
    print(update_room_status(1, "maintenance", 1))
