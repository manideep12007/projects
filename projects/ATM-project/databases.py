import sqlite3 

# creating connection 
connection = sqlite3.connect("atm.db")

# creating cursor to connection 
cursor = connection.cursor()

# creating table if it doesn't exist 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS USERS(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USERNAME TEXT UNIQUE NOT NULL,
        EMAIL TEXT UNIQUE NOT NULL,
        PIN TEXT NOT NULL,
        BALANCE REAL DEFAULT 0.0
    )
    """)

# save changes
connection.commit()