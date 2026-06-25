# Smart Deutsche Bahn Seat Navigator

## Project Overview

Smart Deutsche Bahn Seat Navigator is a Python-based railway seat reservation and journey management system inspired by the German railway network (Deutsche Bahn). The system allows users to search trains, manage passenger information, reserve seats, cancel bookings, monitor seat availability, and generate reports.

The project demonstrates the practical application of Object-Oriented Programming (OOP), SQL database integration, file handling, exception handling, and menu-driven user interaction using Python.

---

## Purpose

The purpose of this project is to provide a simple railway management solution that allows passengers and administrators to manage train journeys and seat reservations efficiently. The system simulates the functionality of a real-world railway reservation platform while demonstrating fundamental Python and database concepts.

---

## Features

### Train Management

- View all available trains
- Search trains between source and destination stations
- Display train details including departure and arrival times
- Check train occupancy levels

### Passenger Management

- Add new passengers
- View passenger records
- Update passenger information
- Delete passenger records

### Reservation Management

- Book train seats
- Cancel reservations
- View all reservations
- Search reservations

### Seat Availability

- Display available seats
- Prevent double booking of seats
- Automatically update seat status after booking or cancellation

### Reporting

- Generate train occupancy reports
- View popular routes
- Export reservation reports to CSV files

### Error Handling

- Invalid menu input handling
- Duplicate email validation
- Invalid seat number validation
- Database exception handling

---

## Technologies Used

- Python 3.x
- SQLite Database
- CSV Module
- Object-Oriented Programming (OOP)

---

## Project Structure

```text
Smart-Deutsche-Bahn-Seat-Navigator/

│
├── program.py
├── deutsche_bahn_project.db
├── reservation_report.csv
└── README.md
```

---

## Classes Used

### DatabaseConnection

Responsible for:

- Creating database tables
- Managing database connections
- Inserting sample train data

### Train

Responsible for:

- Viewing trains
- Searching trains
- Checking seat availability
- Displaying occupancy information

### Passenger

Responsible for:

- Adding passengers
- Viewing passengers
- Updating passenger information
- Deleting passengers

### Reservation

Responsible for:

- Booking seats
- Cancelling bookings
- Viewing reservations
- Searching reservations

### **Report**

Responsible for:

- Generating route reports
- Generating occupancy reports
- Exporting reservation data to CSV files

---

## Database Tables

### trains

| Column         | Description       |
| -------------- | ----------------- |
| train_id       | Unique train ID   |
| train_name     | Train number      |
| train_type     | ICE, IC, RE       |
| source         | Departure station |
| destination    | Arrival station   |
| departure_time | Departure time    |
| arrival_time   | Arrival time      |
| total_seats    | Total seats       |

### passengers

| Column       | Description         |
| ------------ | ------------------- |
| passenger_id | Unique passenger ID |
| name         | Passenger name      |
| phone        | Phone number        |
| email        | Email address       |

### reservations

| Column         | Description           |
| -------------- | --------------------- |
| reservation_id | Unique reservation ID |
| passenger_id   | Passenger reference   |
| train_id       | Train reference       |
| seat_number    | Reserved seat         |
| status         | Booking status        |

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Smart-Deutsche-Bahn-Seat-Navigator.git
```

### Step 2: Open the Project Folder

```bash
cd Smart-Deutsche-Bahn-Seat-Navigator
```

### Step 3: Run the Program

```bash
python program.py
```

---

## Example Usage

### Add Passenger

Input:

```text
Enter passenger name: Ali Khan
Enter phone number: 03001234567
Enter email: ali@gmail.com
```

Output:

```text
Passenger added successfully.
```

### Book Seat

Input:

```text
Passenger ID: 1
Train ID: 1
Seat Number: 10
```

Output:

```text
Seat booked successfully.
```

### Duplicate Booking Attempt

Input:

```text
Passenger ID: 1
Train ID: 1
Seat Number: 10
```

Output:

```text
This seat is already booked.
```

### Export Report

Output:

```text
Reservation report exported successfully.
```

Generated file:

```text
reservation_report.csv
```

---

## Learning Outcomes Demonstrated

This project demonstrates:

- Object-Oriented Programming
- Classes and Objects
- Methods and Functions
- Loops and Conditional Statements
- SQLite Database Integration
- CRUD Operations
- File Handling
- Exception Handling
- Data Validation
- Menu-Driven Application Design
- Report Generation

---

## Future Improvements

Possible future enhancements include:

- User authentication and login system
- Graphical User Interface (GUI)
- Integration with real Deutsche Bahn open data
- Coach-wise seat allocation
- Ticket generation and printing
- Online payment functionality
- Route optimization algorithms
- Real-time train information

---

## Author

**XYZ Name**

Smart Deutsche Bahn Seat Navigator

Python and SQL Railway Reservation System Project
****