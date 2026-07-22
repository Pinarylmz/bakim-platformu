import sqlite3
import bcrypt

db_path = 'backend/maintenance.db'
conn = sqlite3.connect(db_path, timeout=10)
c = conn.cursor()
plain_password = '[AdminPlatformLogin]'
hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
c.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (hashed,))
conn.commit()
print("Direct DB update successful.")
conn.close()
