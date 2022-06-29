import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")
conn.execute('DROP TABLE students')
conn.execute(
    'CREATE TABLE students (name TEXT, ID TEXT, gender TEXT, GPA TEXT)')
print( "Table created successfully")
conn.close()