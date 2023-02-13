import sqlite3
import os
#current_dir = os.getcwd()
#print(current_dir)

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 username TEXT,
                                 password TEXT)''')
conn.commit()
conn.close()