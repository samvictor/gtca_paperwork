"""
  Written by Sam for Glad Tidings School
  This program helps them organize their paperwork digitally
"""
#!/usr/bin/env python

import time
from flask import Flask
from threading import Thread
import webbrowser

print("Hello world, I'm running flask")

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

def start_server():
    app.run(port=1094)

def open_browser():
    time.sleep(3)
    webbrowser.get().open("https://www.google.com")


if __name__ == "__main__":
    server_thr = Thread(target = start_server)
    browse_thr = Thread(target = open_browser)
    server_thr.start()
    browse_thr.start()
