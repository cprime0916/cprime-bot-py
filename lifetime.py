from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Home signal returned."

def run():
    app.run(host='0.0.0.0', port=8080)

def lifetime():
    t = Thread(target=run)
    t.start()