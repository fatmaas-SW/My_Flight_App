import tkinter as tk
from tkinter import messagebox
import sqlite3

root = tk.Tk()
root.title("Flight Reservation System")
root.geometry("400x500")
root.configure(bg="#f0f8ff")  # لون خلفية هادي

label = tk.Label(root, text="Available Flights", font=("Arial", 14), bg="#f0f8ff")
label.pack(pady=10)

text = tk.Text(root, width=50, height=10)
text.pack()

def view_flights():
    conn = sqlite3.connect("flights.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flights")
    rows = cursor.fetchall()
    conn.close()

    text.delete("1.0", tk.END)

    for row in rows:
        flight_info = f"Flight No: {row[1]} | Destination: {row[2]} | Seats Available: {row[3]}\n"
        text.insert(tk.END, flight_info)

btn = tk.Button(root, text="Show Flights", command=view_flights, bg="#4caf50", fg="white")
btn.pack(pady=10)

booking_frame = tk.Frame(root, bg="#f0f8ff")
booking_frame.pack(pady=10)

name_label = tk.Label(booking_frame, text="Your Name:", bg="#f0f8ff")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(booking_frame)
name_entry.grid(row=0, column=1)

flight_label = tk.Label(booking_frame, text="Flight No:", bg="#f0f8ff")
flight_label.grid(row=1, column=0)
flight_entry = tk.Entry(booking_frame)
flight_entry.grid(row=1, column=1)

def book_flight():
    name = name_entry.get()
    flight_no = flight_entry.get()

    if name == "" or flight_no == "":
        messagebox.showwarning("Missing Info", "Please enter your name and flight number.")
        return

    conn = sqlite3.connect("flights.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, seats_available FROM flights WHERE flight_no = ?", (flight_no,))
    flight = cursor.fetchone()

    if flight:
        flight_id, seats = flight
        if seats > 0:
            cursor.execute("UPDATE flights SET seats_available = seats_available - 1 WHERE id = ?", (flight_id,))
            cursor.execute("INSERT INTO reservations (passenger_name, flight_id) VALUES (?, ?)", (name, flight_id))
            conn.commit()
            messagebox.showinfo("Success", f"✅ Booking confirmed for {name} on flight {flight_no}.")
            name_entry.delete(0, tk.END)
            flight_entry.delete(0, tk.END)
            view_flights()
        else:
            messagebox.showerror("Full", "❌ No seats available.")
    else:
        messagebox.showerror("Not Found", "❌ Flight not found.")

    conn.close()

book_btn = tk.Button(root, text="Book Flight", command=book_flight, bg="#2196f3", fg="white")
book_btn.pack(pady=5)

def view_reservations():
    conn = sqlite3.connect("flights.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT reservations.passenger_name, flights.flight_no, flights.destination
    FROM reservations
    JOIN flights ON reservations.flight_id = flights.id
    """)

    rows = cursor.fetchall()
    conn.close()

    text.delete("1.0", tk.END)

    if rows:
        for row in rows:
            text.insert(tk.END, f"{row[0]} booked flight {row[1]} to {row[2]}\n")
    else:
        text.insert(tk.END, "No reservations found.\n")

res_btn = tk.Button(root, text="Show Reservations", command=view_reservations, bg="#9c27b0", fg="white")
res_btn.pack(pady=5)

root.mainloop()