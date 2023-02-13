from flask import Flask, render_template, Request, request, session, redirect, url_for
import sqlite3
app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/')
def index():
    #データベースからのデータ取得
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM jidoukaikan')
    list = c.fetchall()
    conn.close()
    return render_template('index.html', list = list)

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
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))



if __name__ == "__main__":
    app.run(debug=True)