import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shivusql",
    database="Railway"
)
cursor = conn.cursor()

def search_tickets():
    reservationid = reservationid_entry.get()

    try:
        cursor.execute('''SELECT * FROM Tickets
                       LEFT JOIN Reservation ON Tickets.ReservationID = Reservation.ReservationID
                       LEFT join passengers on passengers.PassengerID = reservation.PassengerID
                       WHERE reservation.ReservationID = %s''', (reservationid,))
        td = cursor.fetchone()

        if td:
            messagebox.showinfo("Ticket Details",
                                f'''Ticket ID:{td[0]}
Reservation ID:{td[1]}
Amount:{td[2]}
Reservation id: {td[3]}
Passenger id: {td[4]}
Trainid: {td[5]}
Journey date: {td[6]}
Seat number: {td[7]}
Passenger id: {td[8]}
Name: {td[9]}
Age: {td[10]}
Gender: {td[11]}
Email: {td[12]}
Phone: {td[13]}''')
        else:
            messagebox.showinfo("Ticket Not Found", "Ticket with the given ID not found.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

portal = tk.Tk()
portal.title("Search Tickets")
portal.geometry("400x200")
portal.configure(bg='violet')

label = tk.Label(portal, text="Search Tickets by Reservation ID",bg='violet')
label.pack(pady=10)

reservationid_label = tk.Label(portal, text="Reservation ID:",bg='violet')
reservationid_label.pack()

reservationid_entry = tk.Entry(portal)
reservationid_entry.pack()

search_button = tk.Button(portal, text="Search", command=search_tickets,bg='blue',fg='white')
search_button.pack(pady=10)

portal.mainloop()

# Close the database connection
cursor.close()
conn.close()

