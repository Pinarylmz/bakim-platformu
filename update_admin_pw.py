import sqlite3
import bcrypt
import time

db_path = 'backend/maintenance.db'
conn = sqlite3.connect(db_path, timeout=30)
c = conn.cursor()

# The requested plain text password
plain_password = '[AdminPlatformLogin]'

# Hash the password
hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Update the admin user
c.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (hashed,))
conn.commit()

# Check how many rows were updated
rows_affected = c.rowcount
conn.close()

if rows_affected > 0:
    print(f"Successfully updated password for {rows_affected} user(s).")
else:
    print("Warning: User 'admin' not found or not updated.")
