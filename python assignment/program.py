import sqlite3
import csv


class DatabaseConnection:
    def __init__(self):
        self.connection = sqlite3.connect("deutsche_bahn_project.db")
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS trains (
                train_id INTEGER PRIMARY KEY AUTOINCREMENT,
                train_name TEXT NOT NULL,
                train_type TEXT NOT NULL,
                source TEXT NOT NULL,
                destination TEXT NOT NULL,
                departure_time TEXT NOT NULL,
                arrival_time TEXT NOT NULL,
                total_seats INTEGER NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS passengers (
                passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                passenger_id INTEGER,
                train_id INTEGER,
                seat_number INTEGER,
                status TEXT DEFAULT 'Booked',
                FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id),
                FOREIGN KEY (train_id) REFERENCES trains(train_id)
            )
        """)

        self.connection.commit()

    def insert_sample_data(self):
        trains = [
            ("ICE 100", "ICE", "Berlin Hbf", "Munich Hbf", "08:00", "12:30", 50),
            ("IC 220", "IC", "Frankfurt Hbf", "Cologne Hbf", "10:15", "12:00", 40),
            ("RE 330", "RE", "Hamburg Hbf", "Berlin Hbf", "14:00", "16:20", 35),
            ("ICE 450", "ICE", "Cologne Hbf", "Berlin Hbf", "09:30", "13:45", 60)
        ]

        self.cursor.executemany("""
            INSERT OR IGNORE INTO trains
            (train_name, train_type, source, destination, departure_time, arrival_time, total_seats)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, trains)

        self.connection.commit()

    def close(self):
        self.connection.close()


class Train:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def view_all_trains(self):
        self.cursor.execute("SELECT * FROM trains")
        trains = self.cursor.fetchall()

        print("\n--- Available Deutsche Bahn Trains ---")
        for train in trains:
            print(
                f"ID: {train[0]} | {train[1]} | Type: {train[2]} | "
                f"{train[3]} to {train[4]} | {train[5]} - {train[6]} | "
                f"Seats: {train[7]}"
            )

    def search_train(self, source, destination):
        self.cursor.execute("""
            SELECT * FROM trains
            WHERE source = ? AND destination = ?
        """, (source, destination))

        trains = self.cursor.fetchall()

        if trains:
            print("\n--- Search Results ---")
            for train in trains:
                print(
                    f"ID: {train[0]} | {train[1]} | Type: {train[2]} | "
                    f"{train[3]} to {train[4]} | {train[5]} - {train[6]}"
                )
        else:
            print("No train found for this route.")

    def check_available_seats(self, train_id):
        self.cursor.execute(
            "SELECT total_seats FROM trains WHERE train_id = ?",
            (train_id,)
        )
        result = self.cursor.fetchone()

        if result is None:
            print("Invalid train ID.")
            return

        total_seats = result[0]

        self.cursor.execute("""
            SELECT seat_number FROM reservations
            WHERE train_id = ? AND status = 'Booked'
        """, (train_id,))

        booked_seats = [seat[0] for seat in self.cursor.fetchall()]
        available_seats = []

        for seat in range(1, total_seats + 1):
            if seat not in booked_seats:
                available_seats.append(seat)

        print("\nAvailable Seats:")
        print(available_seats)
        print(f"Total Available Seats: {len(available_seats)}")

    def train_occupancy(self, train_id):
        self.cursor.execute(
            "SELECT total_seats FROM trains WHERE train_id = ?",
            (train_id,)
        )
        result = self.cursor.fetchone()

        if result is None:
            print("Invalid train ID.")
            return

        total_seats = result[0]

        self.cursor.execute("""
            SELECT COUNT(*) FROM reservations
            WHERE train_id = ? AND status = 'Booked'
        """, (train_id,))

        booked_seats = self.cursor.fetchone()[0]
        occupancy = (booked_seats / total_seats) * 100

        print(f"Train Occupancy: {occupancy:.2f}%")

        if occupancy < 50:
            print("Status: Less crowded")
        elif occupancy < 80:
            print("Status: Moderately crowded")
        else:
            print("Status: Highly crowded")


class Passenger:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add_passenger(self, name, phone, email):
        try:
            self.cursor.execute("""
                INSERT INTO passengers (name, phone, email)
                VALUES (?, ?, ?)
            """, (name, phone, email))

            self.connection.commit()
            print("Passenger added successfully.")

        except sqlite3.IntegrityError:
            print("Error: This email already exists.")

    def view_passengers(self):
        self.cursor.execute("SELECT * FROM passengers")
        passengers = self.cursor.fetchall()

        print("\n--- Passengers ---")
        for passenger in passengers:
            print(
                f"ID: {passenger[0]} | Name: {passenger[1]} | "
                f"Phone: {passenger[2]} | Email: {passenger[3]}"
            )

    def update_passenger_phone(self, passenger_id, new_phone):
        self.cursor.execute("""
            UPDATE passengers
            SET phone = ?
            WHERE passenger_id = ?
        """, (new_phone, passenger_id))

        self.connection.commit()
        print("Passenger phone updated successfully.")

    def delete_passenger(self, passenger_id):
        self.cursor.execute("""
            DELETE FROM passengers
            WHERE passenger_id = ?
        """, (passenger_id,))

        self.connection.commit()
        print("Passenger deleted successfully.")


class Reservation:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def book_seat(self, passenger_id, train_id, seat_number):
        self.cursor.execute("""
            SELECT total_seats FROM trains
            WHERE train_id = ?
        """, (train_id,))

        train = self.cursor.fetchone()

        if train is None:
            print("Invalid train ID.")
            return

        total_seats = train[0]

        if seat_number < 1 or seat_number > total_seats:
            print("Invalid seat number.")
            return

        self.cursor.execute("""
            SELECT * FROM reservations
            WHERE train_id = ? AND seat_number = ? AND status = 'Booked'
        """, (train_id, seat_number))

        if self.cursor.fetchone():
            print("This seat is already booked.")
            return

        self.cursor.execute("""
            INSERT INTO reservations (passenger_id, train_id, seat_number, status)
            VALUES (?, ?, ?, 'Booked')
        """, (passenger_id, train_id, seat_number))

        self.connection.commit()
        print("Seat booked successfully.")

    def cancel_booking(self, reservation_id):
        self.cursor.execute("""
            UPDATE reservations
            SET status = 'Cancelled'
            WHERE reservation_id = ?
        """, (reservation_id,))

        self.connection.commit()
        print("Booking cancelled successfully.")

    def view_reservations(self):
        self.cursor.execute("""
            SELECT reservations.reservation_id, passengers.name,
                   trains.train_name, trains.source, trains.destination,
                   reservations.seat_number, reservations.status
            FROM reservations
            JOIN passengers ON reservations.passenger_id = passengers.passenger_id
            JOIN trains ON reservations.train_id = trains.train_id
        """)

        reservations = self.cursor.fetchall()

        print("\n--- Reservations ---")
        for reservation in reservations:
            print(
                f"Reservation ID: {reservation[0]} | Passenger: {reservation[1]} | "
                f"Train: {reservation[2]} | Route: {reservation[3]} to {reservation[4]} | "
                f"Seat: {reservation[5]} | Status: {reservation[6]}"
            )

    def find_reservation(self, reservation_id):
        self.cursor.execute("""
            SELECT * FROM reservations
            WHERE reservation_id = ?
        """, (reservation_id,))

        reservation = self.cursor.fetchone()

        if reservation:
            print(reservation)
        else:
            print("Reservation not found.")


class Report:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def popular_routes(self):
        self.cursor.execute("""
            SELECT trains.source, trains.destination, COUNT(reservations.reservation_id)
            FROM reservations
            JOIN trains ON reservations.train_id = trains.train_id
            WHERE reservations.status = 'Booked'
            GROUP BY trains.source, trains.destination
            ORDER BY COUNT(reservations.reservation_id) DESC
        """)

        routes = self.cursor.fetchall()

        print("\n--- Popular Routes ---")
        for route in routes:
            print(f"{route[0]} to {route[1]} | Bookings: {route[2]}")

    def total_bookings(self):
        self.cursor.execute("""
            SELECT COUNT(*) FROM reservations
            WHERE status = 'Booked'
        """)

        total = self.cursor.fetchone()[0]
        print(f"Total Active Bookings: {total}")

    def export_reservations_csv(self):
        self.cursor.execute("""
            SELECT reservations.reservation_id, passengers.name,
                   trains.train_name, trains.source, trains.destination,
                   reservations.seat_number, reservations.status
            FROM reservations
            JOIN passengers ON reservations.passenger_id = passengers.passenger_id
            JOIN trains ON reservations.train_id = trains.train_id
        """)

        reservations = self.cursor.fetchall()

        with open("reservation_report.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Reservation ID",
                "Passenger",
                "Train",
                "Source",
                "Destination",
                "Seat Number",
                "Status"
            ])
            writer.writerows(reservations)

        print("Reservation report exported successfully.")

    def train_report(self):
        self.cursor.execute("""
            SELECT trains.train_name, trains.train_type, trains.source,
                   trains.destination, trains.total_seats,
                   COUNT(reservations.reservation_id)
            FROM trains
            LEFT JOIN reservations
            ON trains.train_id = reservations.train_id
            AND reservations.status = 'Booked'
            GROUP BY trains.train_id
        """)

        reports = self.cursor.fetchall()

        print("\n--- Train Report ---")
        for report in reports:
            print(
                f"Train: {report[0]} | Type: {report[1]} | "
                f"Route: {report[2]} to {report[3]} | "
                f"Booked Seats: {report[5]}/{report[4]}"
            )


def show_menu():
    print("\n===== Smart Deutsche Bahn Seat Navigator =====")
    print("1. View All Trains")
    print("2. Search Train")
    print("3. Check Available Seats")
    print("4. Add Passenger")
    print("5. View Passengers")
    print("6. Book Seat")
    print("7. Cancel Booking")
    print("8. View Reservations")
    print("9. Train Occupancy")
    print("10. Popular Routes Report")
    print("11. Export Reservation Report")
    print("12. Train Report")
    print("13. Exit")


def main():
    database = DatabaseConnection()
    database.create_tables()
    database.insert_sample_data()

    train = Train(database.connection)
    passenger = Passenger(database.connection)
    reservation = Reservation(database.connection)
    report = Report(database.connection)

    while True:
        show_menu()

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                train.view_all_trains()

            elif choice == 2:
                source = input("Enter source station: ")
                destination = input("Enter destination station: ")
                train.search_train(source, destination)

            elif choice == 3:
                train_id = int(input("Enter train ID: "))
                train.check_available_seats(train_id)

            elif choice == 4:
                name = input("Enter passenger name: ")
                phone = input("Enter phone number: ")
                email = input("Enter email: ")

                if name == "" or phone == "" or email == "":
                    print("All fields are required.")
                else:
                    passenger.add_passenger(name, phone, email)

            elif choice == 5:
                passenger.view_passengers()

            elif choice == 6:
                passenger_id = int(input("Enter passenger ID: "))
                train_id = int(input("Enter train ID: "))
                seat_number = int(input("Enter seat number: "))
                reservation.book_seat(passenger_id, train_id, seat_number)

            elif choice == 7:
                reservation_id = int(input("Enter reservation ID: "))
                reservation.cancel_booking(reservation_id)

            elif choice == 8:
                reservation.view_reservations()

            elif choice == 9:
                train_id = int(input("Enter train ID: "))
                train.train_occupancy(train_id)

            elif choice == 10:
                report.popular_routes()

            elif choice == 11:
                report.export_reservations_csv()

            elif choice == 12:
                report.train_report()

            elif choice == 13:
                print("Thank you for using Smart Deutsche Bahn Seat Navigator.")
                database.close()
                break

            else:
                print("Invalid choice. Please select a valid option.")

        except ValueError:
            print("Invalid input. Please enter a number.")

        except Exception as error:
            print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()