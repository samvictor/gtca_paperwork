"""
  Written by Sam for Glad Tidings School
  This program helps them organize their paperwork digitally
"""
#!/usr/bin/env python
# pip install flask && pip install requests
import time, webbrowser, requests
from flask import Flask, url_for, render_template
from threading import Thread
import shutil

my_port = 1094
scanner_path = "C:\\Users\\Errolyn Fraser\\SCANNER\\"
static_path = "C:\\Users\\Errolyn Fraser\\Documents\\gtca_paperwork\\paper_data\\static\\"

print("Hello world, I'm running flask")

app = Flask(__name__)


# ============== Flask views ==================
@app.route("/")
def hello():
    
    return "Hello World!"
 
@app.route("/viewpdf")
def view_pdf():
    shutil.copy(scanner_path+"scanscan0014.pdf", static_path+"scanner\scanscan0014.pdf")
    to_html = {"to_display":["scanscan0014.pdf", 
                                            "scanscan0013.pdf",
                                            "scanscan0012.pdf"]}
    return render_template('view_pdf.html', data=to_html)


# =============== other functions =============
def start_server():
    app.run(port=my_port)

def open_browser():
    s_code = -1
    while s_code != 200:
        s_code = requests.head("http://localhost:"+str(my_port)).status_code
        time.sleep(0.5)
    webbrowser.open("http://localhost:"+str(my_port)+"/viewpdf")


    
    
if __name__ == "__main__":
    server_thr = Thread(target = start_server)
    browse_thr = Thread(target = open_browser)
    server_thr.start()
    browse_thr.start()



