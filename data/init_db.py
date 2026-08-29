import sqlite3
from pathlib import Path

SCHEMA_DIR = Path('./schema')
conn = sqlite3.connect("./app.db")
conn.execute("PRAGMA foreign_keys = ON")

for file_name in [
    "customers.sql",
    "orders.sql",
    "tickets.sql"
]:
    sql = (SCHEMA_DIR / file_name).read_text()
    conn.executescript(sql)

conn.commit()
conn.close()
