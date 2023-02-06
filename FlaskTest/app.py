from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        # 追加箇所
        text = request.form["input_text"]
        print(text)
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)