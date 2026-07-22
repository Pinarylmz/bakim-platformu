import sqlite3

db_path = 'backend/maintenance.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT id, username, password_hash, approval_status FROM users ORDER BY id DESC LIMIT 5")
users = c.fetchall()
for u in users:
    print(f"ID: {u[0]}, Username: {u[1]}, Hash: {u[2]}, Status: {u[3]}")
conn.close()
