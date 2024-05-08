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

def cancel_ticket():
    reservation_id = reservation_id_entry.get()

    try:
        # Check if reservation exists
        cursor.execute("SELECT * FROM Reservation WHERE ReservationID = %s", (reservation_id,))
        reservation = cursor.fetchone()
        if not reservation:
            messagebox.showerror("Error", "Reservation not found!")
            return

        # Delete ticket details
        cursor.execute("DELETE FROM Tickets WHERE ReservationID = %s", (reservation_id,))

        # Delete reservation details
        cursor.execute("DELETE FROM Reservation WHERE ReservationID = %s", (reservation_id,))

        # Delete passenger details if no other reservations exist for this passenger
        cursor.execute("SELECT COUNT(*) FROM Reservation WHERE PassengerID = %s", (reservation[1],))
        reservation_count = cursor.fetchone()[0]
        if reservation_count == 0:
            cursor.execute("DELETE FROM Passengers WHERE PassengerID = %s", (reservation[1],))

        # Commit changes
        db.commit()
        messagebox.showinfo("Success", "Ticket cancelled successfully!")
    except Exception as e:
        # Rollback if there's any error
        db.rollback()
        messagebox.showerror("Error", str(e))

# Create tkinter window
portal = tk.Tk()
portal.title("Ticket Cancellation Portal")
portal.configure(bg="violet")

# Create labels and entry widgets
tk.Label(portal, text="Reservation ID:", bg="violet").grid(row=0, column=0, sticky="w")
reservation_id_entry = tk.Entry(portal)
reservation_id_entry.grid(row=0, column=1)

# Create cancel button
cancel_button = tk.Button(portal, text="Cancel Ticket", command=cancel_ticket, bg="red", fg="white")
cancel_button.grid(row=1, column=0, columnspan=2, pady=10)

# Run tkinter event loop
portal.mainloop()

# Close cursor and database connection
cursor.close()
db.close()
