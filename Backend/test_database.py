import sqlite3

# Connect to the database (matching DB_NAME in database.py)
connection = sqlite3.connect("users.db")

# Get the names of all tables
cursor = connection.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
""")

tables = cursor.fetchall()

print("Tables created in the database:")

for table in tables:
    print(table[0])

# Close the connection
connection.close()