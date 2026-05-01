# from socket_client import ping, register, login, search_rooms, book_room, get_bookings, checkin, validate_token, checkout, cancel_booking, report_fault, update_room_status

# # ── test all actions ───────────────────────────────────

# if __name__ == "__main__":
#     print("\n── ping ──")
#     print(ping())

#     print("\n── register ──")
#     print(register("S001", "Alice Johnson", "alice@uni.edu.au", "password123"))

#     print("\n── login ──")
#     print(login("S001", "password123"))

#     print("\n── search rooms ──")
#     print(search_rooms("2026-05-10", "10:00", "12:00"))

#     print("\n── book room ──")
#     print(book_room(1, 1, "2026-05-10", "10:00", "12:00"))

#     print("\n── get bookings ──")
#     print(get_bookings(1))

#     print("\n── checkin ──")
#     print(checkin(1, 1))

#     print("\n── validate token ──")
#     print(validate_token("tok_a1b2c3d4e5f6", 1))

#     print("\n── checkout ──")
#     print(checkout(1, 1))

#     print("\n── cancel booking ──")
#     print(cancel_booking(1, 1))

#     print("\n── report fault ──")
#     print(report_fault(1, 1, "Projector not working"))

#     print("\n── update room status ──")
#     print(update_room_status(1, "maintenance", 1))



from flask import Flask, render_template, request, redirect, session

from socket_client import login, register, search_rooms, get_bookings

app = Flask(__name__)
app.secret_key = "secret_key_here"


# HOME PAGE
@app.route('/')
def home():
    return redirect('/login')


# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        university_id = request.form['university_id']
        password = request.form['password']

        response = login(university_id, password)

        if response["status"] == "ok":
            session["user_id"] = response["user_id"]
            session["full_name"] = response["full_name"]
            session["role"] = response["role"]

            return redirect('/dashboard')

        return "Login Failed"

    return render_template("login.html")


# REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        university_id = request.form['university_id']
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']

        response = register(
            university_id,
            full_name,
            email,
            password
        )

        if response["status"] == "ok":
            return redirect('/login')

        return "Registration Failed"

    return render_template("register.html")


# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect('/login')

    return render_template(
        "dashboard.html",
        full_name=session["full_name"]
    )


# BOOKINGS PAGE
@app.route('/bookings')
def bookings():
    if "user_id" not in session:
        return redirect('/login')

    response = get_bookings(session["user_id"])

    bookings_data = response.get("bookings", [])

    return render_template(
        "bookings.html",
        bookings=bookings_data
    )


# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)