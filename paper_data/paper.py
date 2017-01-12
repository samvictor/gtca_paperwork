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
from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time
import win32com.client

my_port = 1094
scanner_path = "C:\\Users\\Errolyn Fraser\\SCANNER\\"
static_path = r"C:\Users\Errolyn Fraser\Google Drive\gtca_paperwork\paper_data\static"

print("Hello world, I'm running flask")

app = Flask(__name__)


# ============== Flask views ==================
@app.route("/")
def hello():
    
    return "Hello World!"
 
@app.route("/viewpdf", defaults={"file_num": 0})
@app.route("/viewpdf/", defaults={"file_num": 0})
@app.route("/viewpdf/<int:file_num>")
def view_pdf(file_num):
    file_num = int(file_num)
    scanner_files = os.listdir(scanner_path)
    files = []
    for file_name in scanner_files:
        file_stats = os.stat(os.path.join(scanner_path, file_name))
        if S_ISREG(file_stats[ST_MODE]):
            files.append({"name": file_name, "time": file_stats[ST_CTIME]})
    
    files = sorted(files, key = lambda file: file["time"], reverse = True)
    file_name = files[file_num]["name"]
    file_name_ns = file_name.replace(" ", "_")
    print(os.path.join(static_path, "scanner", file_name))
    shutil.copyfile(os.path.join(scanner_path, file_name),
                        os.path.join(static_path, "scanner", file_name_ns))
    
    file_ext = file_name_ns.split(".")[-1]
    bad_format = 0
    if file_ext in ["doc", "docx", "ppt", "pptx", "pub", "pubx", "xls", "xlsx"]:
        os.system("start \"\"  \""+ os.path.join(static_path, "scanner", file_name_ns) + "\"")
        bad_format = 1
    
    to_html = {"to_display": file_name_ns, "file_num":  file_num, "max_file_num": len(files) - 1,
                        "bad_format": bad_format }
    return render_template("view_pdf.html", data=to_html)


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



