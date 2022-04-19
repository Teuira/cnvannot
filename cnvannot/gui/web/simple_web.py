from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/", methods=['GET'])
def main_page():
    return render_template('home.html')


@app.route("/", methods=['POST'])
def search():
    return "OK"


def run_server():
    app.run()
