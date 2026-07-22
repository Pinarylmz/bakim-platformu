import sqlite3
import bcrypt

db_path = 'backend/maintenance.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT id, username, password_hash FROM users")
users = c.fetchall()

updated = 0
for u in users:
    uid, username, pwd = u
    if pwd and not pwd.startswith('$'):
        # It's plain text, hash it
        hashed = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        c.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hashed, uid))
        updated += 1
        print(f"Hashed password for user: {username}")

conn.commit()
conn.close()
print(f"Migration complete. {updated} users updated.")
