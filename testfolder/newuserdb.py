import sqlite3
import bcrypt

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create a table to store user information
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

# Hash the plaintext password
password = b"test123"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

# Insert a new user into the database
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('etasos', hashed))

# Commit the changes and close the connection
conn.commit()
conn.close()