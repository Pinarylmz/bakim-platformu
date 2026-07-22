import sqlite3
db_path = 'backend/maintenance.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("UPDATE users SET approval_status = 'Approved', role = 'Technician' WHERE username = 'testuser1234'")
conn.commit()
conn.close()
