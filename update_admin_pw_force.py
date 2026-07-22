import sqlite3
import bcrypt
import shutil
import time

db_path = 'backend/maintenance.db'
temp_db_path = 'backend/maintenance_temp.db'

# Copy the locked DB
shutil.copy2(db_path, temp_db_path)

conn = sqlite3.connect(temp_db_path)
c = conn.cursor()

# The requested plain text password
plain_password = '[AdminPlatformLogin]'

# Hash the password
hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Update the admin user
c.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (hashed,))
conn.commit()
rows_affected = c.rowcount
conn.close()

if rows_affected > 0:
    # Overwrite the original DB
    try:
        shutil.copy2(temp_db_path, db_path)
        print(f"Successfully updated password for {rows_affected} user(s) via shadow copy.")
    except Exception as e:
        print(f"Failed to overwrite original DB: {e}")
else:
    print("Warning: User 'admin' not found or not updated.")
