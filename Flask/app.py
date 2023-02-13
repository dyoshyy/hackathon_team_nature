from flask import Flask, render_template, Request, request
import sqlite3
app = Flask(__name__)

@app.route('/')
def index():
    #データベースからのデータ取得
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('SELECT * FROM jidoukaikan')
    list = c.fetchall()
    conn.close()
    return render_template('index.html', list = list)

@app.route('/login_top')
def login_top():
    return render_template('login.html')

@app.route('/login',methods=["POST"])
def login():
    name = request.form['name']
    password = request.form['pass']
    return render_template('login_result.html', name = name, password = password)


if __name__ == "__main__":
    app.run(debug=True)