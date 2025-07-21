import sqlite3
# إنشاء قاعدة البيانات
conn = sqlite3.connect("flights.bd")
cursor = conn.cursor()

# جدول الرحلات
cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_no TEXT NOT NULL,
    destination TEXT NOT NULL,
    seats_available INTEGER NOT NULL
)
""")

# جدول الحجوزات
cursor.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_name TEXT NOT NULL,
    flight_id INTEGER,
    FOREIGN KEY (flight_id) REFERENCES flights(id)
)
""")

# إضافة بيانات مبدئية
cursor.execute("INSERT INTO flights (flight_no, destination, seats_available) VALUES ('MS123', 'Cairo', 5)")
cursor.execute("INSERT INTO flights (flight_no, destination, seats_available) VALUES ('MS456', 'Dubai', 3)")

conn.commit()
conn.close()

print("Database created and filled successfully!")