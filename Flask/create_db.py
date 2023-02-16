import sqlite3
import os
#current_dir = os.getcwd()
#print(current_dir)

conn = sqlite3.connect('board.db')
c = conn.cursor()


#c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                 username TEXT,
#                                 password TEXT,
#                                 gender TEXT,
#                                 mail TEXT)''')

for area in ['chuo','kita','minami','higashi','nishi','atsubetsu','toyohira','kiyota','teine','shiroishi']:

    table_name = 'board_' + area
    c.execute(f'''CREATE TABLE {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            author TEXT,
                                            content TEXT,
                                            date TEXT
                                            )''')

conn.commit()
conn.close()