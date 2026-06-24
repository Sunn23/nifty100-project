import sqlite3

conn = sqlite3.connect("nifty100.db")

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM companies")

print("Companies:", cursor.fetchone()[0])

conn.close()

conn = sqlite3.connect("nifty100.db")

cursor = conn.cursor()
cursor.execute("PRAGMA foreaign_key_check")
rows= cursor.fetchall()

print(rows)

conn.close()