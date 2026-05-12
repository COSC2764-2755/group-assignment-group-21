from flask import Flask, render_template, request, redirect, session
from socket_client import (
    login, register, search_rooms, get_bookings,
    book_room, cancel_booking, checkin, checkout
)

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
        password      = request.form['password']

        response = login(university_id, password)

        if response["status"] == "ok":
            session["user_id"]   = response["user_id"]
            session["full_name"] = response["full_name"]
            session["role"]      = response["role"]
            return redirect('/dashboard')

        return render_template("login.html", error=response.get("message", "Login failed."))

    return render_template("login.html")


# REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        university_id = request.form['university_id']
        full_name     = request.form['full_name']
        email         = request.form['email']
        password      = request.form['password']

        response = register(university_id, full_name, email, password)

        if response["status"] == "ok":
            return redirect('/login')

        return render_template("register.html", error=response.get("message", "Registration failed."))

    return render_template("register.html")


# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect('/login')
    return render_template("dashboard.html", full_name=session["full_name"])


# SEARCH ROOMS PAGE
@app.route('/search_rooms', methods=['GET', 'POST'])
def search_rooms_page():
    if "user_id" not in session:
        return redirect('/login')

    rooms = []
    date       = ""
    start_time = ""
    end_time   = ""

    if request.method == 'POST':
        date       = request.form['date']
        start_time = request.form['start_time']
        end_time   = request.form['end_time']

        # Store search params in session so book_room can use them
        session["search_date"]       = date
        session["search_start_time"] = start_time
        session["search_end_time"]   = end_time

        response = search_rooms(date, start_time, end_time)

        if response["status"] == "ok":
            rooms = response["rooms"]
        else:
            return render_template("search_rooms.html", rooms=[], error=response.get("message"))

    return render_template(
        "search_rooms.html",
        rooms=rooms,
        date=date,
        start_time=start_time,
        end_time=end_time
    )


# BOOK ROOM
@app.route('/book_room/<int:room_id>')
def book_room_page(room_id):
    if "user_id" not in session:
        return redirect('/login')

    # Pull the date/time that was searched — must have searched first
    date       = session.get("search_date")
    start_time = session.get("search_start_time")
    end_time   = session.get("search_end_time")

    if not all([date, start_time, end_time]):
        return redirect('/search_rooms')

    response = book_room(
        session["user_id"],
        room_id,
        date,
        start_time,
        end_time
    )

    if response["status"] == "ok":
        token = response["token"]
        return render_template("booking_confirmed.html", token=token, date=date,
                               start_time=start_time, end_time=end_time)

    return render_template("search_rooms.html", rooms=[], error=response.get("message", "Booking failed."))


# MY BOOKINGS PAGE
@app.route('/bookings')
def bookings_page():
    if "user_id" not in session:
        return redirect('/login')

    response = get_bookings(session["user_id"])
    bookings_data = response.get("bookings", [])

    return render_template("bookings.html", bookings=bookings_data)


# CANCEL BOOKING
@app.route('/cancel_booking/<int:booking_id>')
def cancel_booking_page(booking_id):
    if "user_id" not in session:
        return redirect('/login')

    response = cancel_booking(booking_id, session["user_id"])

    # Redirect back to bookings regardless, show error there if needed
    return redirect('/bookings')


# CHECK IN
@app.route('/checkin/<int:booking_id>')
def checkin_page(booking_id):
    if "user_id" not in session:
        return redirect('/login')

    response = checkin(booking_id, session["user_id"])

    if response["status"] == "ok":
        return f"Checked in successfully for booking #{booking_id}. <a href='/bookings'>Back to bookings</a>"

    return f"Check-in failed: {response.get('message')}. <a href='/bookings'>Back</a>"


# CHECK OUT
@app.route('/checkout/<int:booking_id>')
def checkout_page(booking_id):
    if "user_id" not in session:
        return redirect('/login')

    response = checkout(booking_id, session["user_id"])

    if response["status"] == "ok":
        return f"Checked out successfully. Room returned. <a href='/bookings'>Back to bookings</a>"

    return f"Check-out failed: {response.get('message')}. <a href='/bookings'>Back</a>"


# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
