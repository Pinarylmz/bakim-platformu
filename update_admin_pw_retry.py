import sqlite3
import bcrypt
import time

db_path = 'backend/maintenance.db'
plain_password = '[AdminPlatformLogin]'
hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

success = False
for _ in range(10):
    try:
        conn = sqlite3.connect(db_path, timeout=5)
        c = conn.cursor()
        c.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (hashed,))
        conn.commit()
        if c.rowcount > 0:
            print(f"Successfully updated admin password to: {hashed}")
            success = True
        conn.close()
        break
    except sqlite3.OperationalError as e:
        print("Locked, waiting...")
        time.sleep(1)

if not success:
    print("Could not get lock to update the DB directly.")
