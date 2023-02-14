from flask import Flask, render_template, Request, request, session, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boards.db'
db = SQLAlchemy(app)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    messages = db.relationship('Message', backref='board', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)

@app.route('/')
def index():
    #データベースからのデータ取得
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM jidoukaikan')
    list = c.fetchall()
    conn.close()
    username = session.get('username')
    if username:
        pass
    else:
        username = ''
    
    return render_template('index.html', list = list, username = username)

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
def chat():
    if 'user_id' in session:
        username = session.get('username')
        return render_template('chat_top.html', username= username)
    return redirect(url_for('login'))

@app.route('/board/<name>')
def board(name):
    board = Board.query.filter_by(name=name).first()
    messages = Message.query.filter_by(board=board).all()
    return render_template('chat.html', board=board, messages=messages)


if __name__ == "__main__":
    app.run(debug=True)