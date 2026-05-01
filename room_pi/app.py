from socket_client import get_room_info, validate_token, save_sensor_reading, report_fault


if __name__ == "__main__":
    print("\n── get room info ──")
    print(get_room_info(1))

    print("\n── validate token ──")
    print(validate_token("tok_a1b2c3d4e5f6", 1))

    print("\n── save sensor reading ──")
    print(save_sensor_reading(1, 22.5, 55.3, 1013.2))

    print("\n── report fault ──")
    print(report_fault(1, "AC making loud noise"))
