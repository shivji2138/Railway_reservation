import tkinter as tk
import subprocess

#fn to redirect
def show_search_page():
    subprocess.Popen(["python", "search_tickets.py"])

def show_reserve_page():
    subprocess.Popen(["python", "reserve_tickets.py"])

def show_cancel_page():
    subprocess.Popen(["python", "cancel_tickets.py"])

#tkinter window
portal = tk.Tk()
portal.title("Railway Reservation System")
portal.geometry("400x200")
portal.configure(bg='violet')

#gui components

label_home = tk.Label(portal, text="Welcome to Railway Reservation System",bg='violet')
label_home.pack(pady=20)

search_button = tk.Button(portal, text="Search Tickets", command=show_search_page,bg='red',fg='white')
search_button.pack(pady=5)

reserve_button = tk.Button(portal, text="Reserve Tickets", command=show_reserve_page,bg='red',fg='white')
reserve_button.pack(pady=5)

cancel_button = tk.Button(portal, text="Cancel Tickets", command=show_cancel_page,bg='red',fg='white')
cancel_button.pack(pady=5)

portal.mainloop()
