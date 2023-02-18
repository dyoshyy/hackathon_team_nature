from flask import Flask, render_template, Request, request, session, redirect, url_for
import sqlite3
import datetime
from geo import get_lat_lon_from_address
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

app = Flask(__name__)
app.secret_key = 'your-secret-key'

def get_db_connection():
    conn = sqlite3.connect('board.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.teardown_appcontext
def close_db_connection(exception):
    conn = get_db_connection()
    conn.close()

@app.route('/',methods=['GET', 'POST'])
def index():

    #データベースからのデータ取得
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    if request.method == 'POST':

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
        for address in address_list:
            location = geolocator.geocode(address)
            if location:
                latlons.append((location.latitude,location.longitude))
                #print(location.latitude,location.longitude)
        
        print(latlons)

        c.execute('SELECT * FROM jidoukaikan')
        table_jidoukaikan = c.fetchall()
        c.execute('SELECT * FROM event')
        table_event = c.fetchall()
        #c.execute('SELECT * FROM event' + query2)
        #table_event = c.fetchall()

    else:
        c.execute('SELECT * FROM jidoukaikan')
        table_jidoukaikan = c.fetchall()
        c.execute('SELECT * FROM event')
        table_event = c.fetchall()

    conn.close()

    #上部に表示するユーザー名の取得
    username = session.get('username')
    if username:
        pass
    else:
        username = ''
    
    return render_template('index.html', table1 = table_jidoukaikan,table2 = table_event, username = username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['username'] = username
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        gender = request.form['gender']
        mail = request.form['mail']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password, gender, mail) VALUES (?, ?, ?, ?)', (username, password, gender, mail))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/chat')
def chat_top():
    if 'user_id' in session:
        username = session.get('username')
        return render_template('chat_top.html', username= username)
    return redirect(url_for('login'))

@app.route('/board/<name>', methods=['GET', 'POST'])
def chat(name):
    conn = get_db_connection()
    username = session.get('username')
    
    if name == 'chuo':
        board_name = "中央区"
    elif name == 'kita':
        board_name = "北区"    
    elif name == 'minami':
        board_name = "南区"  
    elif name == 'nishi':
        board_name = "西区"  
    elif name == 'higashi':
        board_name = "東区"  
    elif name == 'atsubetsu':
        board_name = "厚別区"  
    elif name == 'toyohira':
        board_name = "豊平区"  
    elif name == 'kiyota':
        board_name = "清田区"  
    elif name == 'teine':
        board_name = "手稲区"  
    elif name == 'shiroishi':
        board_name = "白石区"  
    board_name = board_name + "の掲示板"
    if username:
        pass
    else:
        username = ''
    if request.method == 'POST':
        author = session.get('username')
        content = request.form['content']
        date = datetime.datetime.now()
        c = conn.cursor()
        c.execute(f'INSERT INTO board_{name} (author, content, date) VALUES (?, ?, ?)', (author, content, date))
        conn.commit()
    c = conn.cursor()
    c.execute(f'SELECT * FROM board_{name} ORDER BY id DESC')
    posts = c.fetchall()
    conn.close()
    return render_template('chat.html', posts=posts, username = username, route = "/board/"+name, board_name = board_name)

if __name__ == "__main__":
    app.run(debug=True)