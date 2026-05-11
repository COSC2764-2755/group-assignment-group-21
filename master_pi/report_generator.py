import matplotlib.pyplot as plt


def generate_report():
    rooms = ["A201", "B101", "C301", "D105"]
    bookings = [12, 8, 15, 10]

    plt.figure(figsize=(8, 5))
    plt.bar(rooms, bookings)

    plt.title("Room Booking Frequency Report")
    plt.xlabel("Room Number")
    plt.ylabel("Number of Bookings")

    plt.savefig("report.png")

    print("Report generated successfully: report.png")


if __name__ == "__main__":
    generate_report()