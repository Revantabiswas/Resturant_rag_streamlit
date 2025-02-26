import sqlite3

def init_db():
    conn = sqlite3.connect('restaurant_bookings.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            number_of_people INTEGER,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_booking(date, number_of_people, status="Pending"):
    conn = sqlite3.connect('restaurant_bookings.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (date, number_of_people, status)
        VALUES (?, ?, ?)
    ''', (date, number_of_people, status))
    conn.commit()
    conn.close()

def get_bookings():
    conn = sqlite3.connect('restaurant_bookings.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    bookings = cursor.fetchall()
    conn.close()
    return bookings

def update_booking_status(booking_id, status):
    conn = sqlite3.connect('restaurant_bookings.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE bookings
        SET status = ?
        WHERE id = ?
    ''', (status, booking_id))
    conn.commit()
    conn.close()
