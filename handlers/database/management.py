import sqlite3
import datetime

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS submitted_users (
        user_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

def has_user_submitted(user_id):
    cursor.execute("DELETE FROM submitted_users WHERE timestamp < ?", (datetime.datetime.now() - datetime.timedelta(days=1),))
    conn.commit()
    cursor.execute("SELECT * FROM submitted_users WHERE user_id = ?", (user_id,))
    return cursor.fetchone() is not None

def add_user_to_submitted(user_id):
    cursor.execute("INSERT INTO submitted_users (user_id) VALUES (?)", (user_id,))
    conn.commit()