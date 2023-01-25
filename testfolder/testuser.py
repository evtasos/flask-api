import sqlite3
import bcrypt
def execute(sql, params=()):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    result = cursor.execute(sql, params)
    conn.commit()
    return result

def check_credentials(username, password):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    result = execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed)).fetchone()
    if result:
        return True
    return False

username = 'it21122'
password = b'21122'
print(check_credentials(username, password))
