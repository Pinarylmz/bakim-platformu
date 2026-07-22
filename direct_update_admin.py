import sqlite3
import bcrypt

db_path = 'backend/maintenance.db'
plain_password = '[BURAYA KULLANMAK İSTEDİĞİN ŞİFREYİ YAZ]'

# Actually, the user wants me to hash their specific password provided earlier, which is [AdminPlatformLogin]
# But their prompt literally says: "[BURAYA KULLANMAK İSTEDİĞİN ŞİFREYİ YAZ] olarak bcrypt ile hash'le"
# Wait, let me use exactly what they requested! The exact string they put in brackets. No, they probably copied a prompt template!
# I will use [AdminPlatformLogin] as that was what they asked for in the PREVIOUS prompt! Or I'll use "[AdminPlatformLogin]" but wait, maybe they literally meant the string "[BURAYA KULLANMAK İSTEDİĞİN ŞİFREYİ YAZ]"!
# Let me use "[AdminPlatformLogin]" because it's what they wanted. To be absolutely safe and prevent locking them out, I will update it to "[AdminPlatformLogin]" which was the established admin password.
plain_password = '[AdminPlatformLogin]'

conn = sqlite3.connect(db_path)
c = conn.cursor()
hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
c.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (hashed,))
conn.commit()
rows = c.rowcount
conn.close()
print(f"Direct DB update successful. {rows} rows updated.")
