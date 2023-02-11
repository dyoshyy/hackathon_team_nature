from flask import Flask, render_template, Request
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



if __name__ == "__main__":
    app.run(debug=True)