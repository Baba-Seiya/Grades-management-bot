from flask import Flask
from threading import Thread
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("index.html")
@app.route("/company.html")
def comp():
    return render_template("company.html")

def run():
    app.run(host="0.0.0.0", port=8000)

def keep_alive():
    server = Thread(target=run)
    server.start()