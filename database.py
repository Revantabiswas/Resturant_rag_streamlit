import sqlite3
import os
from datetime import datetime

def init_db():
    """Initialize the SQLite database with tables"""
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    
    # Create reservations table with time slots
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        time TEXT,
        guests INTEGER,
        name TEXT,
        email TEXT,
        phone TEXT,
        special_requests TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def add_booking(date, time, guests, name='', email='', phone='', special_requests=''):
    """Add a new booking to the database"""
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO reservations (date, time, guests, name, email, phone, special_requests) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (date, time, guests, name, email, phone, special_requests)
    )
    
    conn.commit()
    conn.close()
    return True

def get_bookings(date=None, time=None):
    """Get all bookings or filter by date and time"""
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    
    query = 'SELECT * FROM reservations'
    params = []
    
    if date and time:
        query += ' WHERE date = ? AND time = ?'
        params = [date, time]
    elif date:
        query += ' WHERE date = ?'
        params = [date]
    
    cursor.execute(query, params)
    bookings = cursor.fetchall()
    conn.close()
    
    return bookings

def check_availability(date, time, party_size):
    """Check if a reservation can be made for given date, time and party size"""
    max_capacity = 50  # Get from configuration
    
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    
    # Get total guests for that time slot
    cursor.execute('SELECT SUM(guests) FROM reservations WHERE date = ? AND time = ?', (date, time))
    result = cursor.fetchone()
    current_guests = result[0] if result[0] else 0
    
    conn.close()
    
    # Check if adding party_size would exceed capacity
    return (current_guests + party_size <= max_capacity, max_capacity - current_guests)
