import sqlite3
import os
from geopy.geocoders import Nominatim
#current_dir = os.getcwd()
#print(current_dir)

conn = sqlite3.connect('database.db')
c = conn.cursor()


c.execute('SELECT region FROM jidoukaikan')
address_list = c.fetchall()
address_list = list(address_list)

latlons = []
for i,address in enumerate(address_list):
            add = address[0]
            #print(address)
            if '札幌市' not in add:
                add = '札幌市' + str(add)
            if '北海道' not in add:
                add = '北海道' + str(add)
            pos = add.find('丁目') + 2
            add = add[:pos]
            address_list[i] = add
geolocator = Nominatim(user_agent="user-id")
for i,address in enumerate(address_list):
    location = geolocator.geocode(address)
    if location:
        latlons.append((location.latitude,location.longitude))
        value = (location.latitude,location.longitude)
        print(i,location.latitude,location.longitude)
    else:
        latlons.append(None)
        value = (None,None)
        print('None')

    c.execute('''UPDATE jidoukaikan set lat = (?) where id = (?)''', (value[0],i)) 
    c.execute('''UPDATE jidoukaikan set lon = (?) where id = (?)''', (value[1],i)) 

#for area in ['chuo','kita','minami','higashi','nishi','atsubetsu','toyohira','kiyota','teine','shiroishi']:
#
#    table_name = 'board_' + area
#    c.execute(f'''CREATE TABLE {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                            author TEXT,
#                                            content TEXT,
#                                            date TEXT
#                                            )''')

conn.commit()
conn.close()