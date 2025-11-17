import sqlite3

conn = sqlite3.connect("traffic.db")
cur = conn.cursor()

for row in cur.execute("SELECT * FROM readings;"):
    print(row)

conn.close()
