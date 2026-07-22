import sqlite3

db_path = 'backend/maintenance.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT password_hash FROM users WHERE username = 'admin'")
res = c.fetchone()
print(f"Current hash: {res[0] if res else 'None'}")
