import sqlite3
import bcrypt

db_path = 'backend/maintenance.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Set without brackets
plain_password = 'AdminPlatformLogin'
hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

c.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (hashed,))
conn.commit()
rows = c.rowcount
conn.close()
print(f"Updated password to AdminPlatformLogin (without brackets). {rows} rows affected.")
