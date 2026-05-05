from flask import Flask, render_template, request
from socket_client import (
    get_room_info,
    validate_token,
    save_sensor_reading,
    report_fault
)

app = Flask(__name__)


# HOME PAGE
@app.route('/')
def home():
    return """
    <h2>Room Pi System</h2>
    <ul>
        <li><a href="/verify_token">Verify Room Access Token</a></li>
        <li><a href="/room_info">View Room Information</a></li>
        <li><a href="/report_fault">Report Fault</a></li>
    </ul>
    """


# VERIFY TOKEN PAGE
@app.route('/verify_token', methods=['GET', 'POST'])
def verify_token_page():
    if request.method == 'POST':
        token = request.form['token']

        response = validate_token(token, 1)

        if response["status"] == "ok":
            return "Access Granted"

        return "Access Denied"

    return render_template("verify_token.html")


# ROOM INFO PAGE
@app.route('/room_info')
def room_info():
    response = get_room_info(1)

    return f"""
    <h2>Room Information</h2>
    <p>Status: {response.get('status', 'Unknown')}</p>
    <p>Next Booking: {response.get('next_booking', 'No upcoming booking')}</p>
    <a href="/">Back</a>
    """


# REPORT FAULT PAGE
@app.route('/report_fault', methods=['GET', 'POST'])
def report_fault_page():
    if request.method == 'POST':
        issue = request.form['issue']

        response = report_fault(
            1,
            issue
        )

        if response["status"] == "ok":
            return "Fault Report Submitted Successfully"

        return "Failed to Report Fault"

    return """
    <h2>Report Room Fault</h2>
    <form method="POST">
        <input
            type="text"
            name="issue"
            placeholder="Describe the issue"
            required
        >
        <button type="submit">
            Submit Fault Report
        </button>
    </form>
    <br>
    <a href="/">Back</a>
    """


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5002
    )