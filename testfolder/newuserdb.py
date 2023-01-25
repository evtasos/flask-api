import sqlite3
import bcrypt

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
username = 'etasos'
password = "21122"
psw = b'21122'
# Create a table to store user information
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, salt TEXT)''')

# Hash the plaintext password
password = "21122"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode(), salt)

# Insert a new user into the database
cursor.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)", (username, hashed, salt))

# Commit the changes and close the connection
conn.commit()
conn.close()
print(password,password.encode())