from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template('home.html')


def run_server():
    app.run()
