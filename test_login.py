import sqlite3
import bcrypt

db_path = 'backend/maintenance.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT username, password_hash, is_active, approval_status FROM users WHERE username = 'admin'")
user = c.fetchone()
if not user:
    print("User 'admin' not found in database!")
else:
    print(f"User found: username={user[0]}, is_active={user[2]}, approval_status={user[3]}")
    db_hash = user[1]
    print(f"Hash in DB: {db_hash}")
    print(f"Hash type: {type(db_hash)}")
    
    input_pw = '[AdminPlatformLogin]'
    input_encoded = input_pw.encode('utf-8')
    hash_encoded = db_hash.encode('utf-8') if isinstance(db_hash, str) else db_hash
    
    print(f"Input encoded: {input_encoded}")
    print(f"Hash encoded: {hash_encoded}")
    
    try:
        match = bcrypt.checkpw(input_encoded, hash_encoded)
        print(f"Password match: {match}")
    except Exception as e:
        print(f"Bcrypt error: {e}")
