import sqlite3

def execute(sql, params=()):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    result = cursor.execute(sql, params)
    conn.commit()
    return result

def check_credentials(username, password):
    # Connect to the database and check if the provided credentials match the ones stored
    result = execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    if result:
        return True
    return False
username = 'etasos'
password = 'test123'
print(check_credentials(username, password))
