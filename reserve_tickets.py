import mysql.connector
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shivusql",
    database="Railway"
)

# Create cursor
cursor = db.cursor()

def get_available_seats(train_id, journey_date):
    # Fetch reserved seat numbers for the given train and journey date
    reserved_seat_query = "SELECT SeatNumber FROM Reservation WHERE TrainID = %s AND JourneyDate = %s"
    cursor.execute(reserved_seat_query, (train_id, journey_date))
    reserved_seats = set(row[0] for row in cursor.fetchall())

    # Fetch total number of seats for the given train
    total_seat_query = "SELECT AvailableSeats FROM Train WHERE TrainID = %s"
    cursor.execute(total_seat_query, (train_id,))
    total_seats = cursor.fetchone()[0]

    # Generate available seat numbers
    available_seats = [str(i) for i in range(1, total_seats + 1) if str(i) not in reserved_seats]
    return available_seats

def reserve_ticket():
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    train_id = train_id_entry.get()
    journey_date = journey_date_entry.get()

    try:
        # Get available seat numbers
        available_seats = get_available_seats(train_id, journey_date)
        
        # Check if there are enough available seats
        if len(available_seats) == 0:
            messagebox.showerror("Error", "No available seats!")
            return

        # Take the first available seat
        seat_number = available_seats[0]

        # Insert passenger details
        passenger_query = "INSERT INTO Passengers (Name, Age, Gender, Email, Phone) VALUES (%s, %s, %s, %s, %s)"
        passenger_data = (name, age, gender, email, phone)
        cursor.execute(passenger_query, passenger_data)
        passenger_id = cursor.lastrowid

        # Insert reservation details
        reservation_query = "INSERT INTO Reservation (PassengerID, TrainID, JourneyDate, SeatNumber) VALUES (%s, %s, %s, %s)"
        reservation_data = (passenger_id, train_id, journey_date, seat_number)
        cursor.execute(reservation_query, reservation_data)
        reservation_id = cursor.lastrowid

        # Fetch amount from Train table
        train_query = "SELECT Amount FROM Train WHERE TrainID = %s"
        cursor.execute(train_query, (train_id,))
        amount = cursor.fetchone()[0]

        # Calculate total amount for this ticket
        total_amount = amount

        # Insert ticket details
        ticket_query = "INSERT INTO Tickets (ReservationID, Amount) VALUES (%s, %s)"
        ticket_data = (reservation_id, total_amount)
        cursor.execute(ticket_query, ticket_data)

        # Commit changes
        db.commit()

        # Show success message with reservation ID and seat number
        messagebox.showinfo("Success", f"Ticket reserved successfully!\nReservation ID: {reservation_id}, Seat Number: {seat_number}")
        
    except Exception as e:
        # Rollback if there's any error
        db.rollback()
        messagebox.showerror("Error", str(e))


# Create tkinter window
portal = tk.Tk()
portal.title("Ticket Reservation Portal")
portal.configure(bg="violet")
portal.geometry('300x200')

# Create labels
name_label = tk.Label(portal, text="Name:", bg="violet")
name_label.grid(row=0, column=0, sticky="w")

age_label = tk.Label(portal, text="Age:", bg="violet")
age_label.grid(row=1, column=0, sticky="w")

gender_label = tk.Label(portal, text="Gender:", bg="violet")
gender_label.grid(row=2, column=0, sticky="w")

email_label = tk.Label(portal, text="Email:", bg="violet")
email_label.grid(row=3, column=0, sticky="w")

phone_label = tk.Label(portal, text="Phone:", bg="violet")
phone_label.grid(row=4, column=0, sticky="w")

train_id_label = tk.Label(portal, text="Train ID:", bg="violet")
train_id_label.grid(row=5, column=0, sticky="w")

journey_date_label = tk.Label(portal, text="Journey Date (YYYY-MM-DD):", bg="violet")
journey_date_label.grid(row=6, column=0, sticky="w")

# Create entry widgets
name_entry = tk.Entry(portal)
name_entry.grid(row=0, column=1)

age_entry = tk.Entry(portal)
age_entry.grid(row=1, column=1)

gender_entry = tk.Entry(portal)
gender_entry.grid(row=2, column=1)

email_entry = tk.Entry(portal)
email_entry.grid(row=3, column=1)

phone_entry = tk.Entry(portal)
phone_entry.grid(row=4, column=1)

train_id_entry = tk.Entry(portal)
train_id_entry.grid(row=5, column=1)

journey_date_entry = tk.Entry(portal)
journey_date_entry.grid(row=6, column=1)

# Create reserve button
reserve_button = tk.Button(portal, text="Reserve Ticket", command=reserve_ticket, bg="green", fg="white")
reserve_button.grid(row=7, column=0, columnspan=2, pady=10)

# Run tkinter event loop
portal.mainloop()

# Close cursor and database connection
cursor.close()
db.close()

