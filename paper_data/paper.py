"""
  Written by Sam for Glad Tidings School
  This program helps them organize their paperwork digitally
"""
#!/usr/bin/env python
# pip install flask && pip install requests
import time, webbrowser, requests
from flask import Flask, url_for, render_template, redirect, send_from_directory
from threading import Thread
import shutil
from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time
import win32com.client

my_port = 1094

# see if another instance is running
try:
    if requests.head("http://localhost:"+str(my_port)).status_code in [200, 301, 302]:
        print("Program already running")
        webbrowser.open("http://localhost:"+str(my_port))
        time.sleep(5)
        quit()
except requests.exceptions.ConnectionError:
    pass

app = Flask(__name__)
app.secret_key  = os.urandom(25)
#app.use_x_sendfile = True
        
scanner_path = "C:\\Users\\Errolyn Fraser\\SCANNER"
static_path = r"C:\Users\Errolyn Fraser\Google Drive\gtca_paperwork\paper_data\static"
files_path = r"C:\Users\Errolyn Fraser\Google Drive\gtca_paperwork\paper_data\static\paper_files"
static_files_path = r"/static/paper_files"
sep = "\\" # directory separator
print("Hello world, I'm running flask")


# ============== Flask views ==================
@app.route("/", defaults={"dir_path": None})
@app.route("/files/", defaults={"dir_path": None})
@app.route("/files", defaults={"dir_path": None})
@app.route("/files/<path:dir_path>")
def dir_viewer(dir_path):
    if not dir_path:
        curr_path = files_path
        dir_path = ""
    else:      
        # dir_path should always have a trailing slash but never a slash in the beginning
        # if dir_path is blank, no slash
        if dir_path[-1] != "/":
            dir_path += "/"
        # replace '/' with whatever is the separator on this os, and replace spaces with underscores
        # python's replace uses a string while js's replace uses regex
        curr_path = os.path.join(files_path, *dir_path.replace(" ", "_").split("/"))
        
    try:
        files = next(os.walk(curr_path)) # (dirpath, dirnames, filenames)
    except:
        print ("file path "+ curr_path +" not found")
        return redirect(url_for("dir_viewer"), code=302)
        
    to_template = {"folders": files[1], "files": files[2], "curr_path": curr_path, "view_file_path": "/viewfile/" + dir_path}
    return render_template("home.html", data = to_template)
    
    
@app.route("/servefiles/<path:file_path>")
def serve_file(file_path):
     return send_from_directory(static_files_path, file_path.replace("/", "\\"))
    
@app.route("/viewfile/<path:file_path>")
def file_viewer(file_path):
    file_path = static_files_path + "/" + file_path
    
    to_template = {"file_path": file_path, "bad_format": 0, "time": str(time.time())}
    return render_template("view_pdf.html", data = to_template)
    
    
 
@app.route("/viewnew", defaults={"file_num": 0})
@app.route("/viewnew/", defaults={"file_num": 0})
@app.route("/viewnew/<int:file_num>")
def view_new_pdf(file_num):
    file_num = int(file_num)
    scanner_files = next(os.walk(scanner_path))[2]
    #scanner_files = os.listdir(scanner_path)
    files = []
    for file_name in scanner_files:
        file_stats = os.stat(os.path.join(scanner_path, file_name))
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
                        "bad_format": bad_format, "time": str(time.time())}
    return render_template("view_new.html", data=to_html)


# =============== other functions =============
def start_server():
    app.run(port=my_port)

def open_browser():
    s_code = -1
    while s_code not in [200, 301, 302]:
        try:
            s_code = requests.head("http://localhost:"+str(my_port)).status_code
        except requests.exceptions.ConnectionError:
            print("connection refused. Trying again.")
        time.sleep(0.5)
    webbrowser.open("http://localhost:"+str(my_port))


    
    
if __name__ == "__main__":
    server_thr = Thread(target = start_server)
    browse_thr = Thread(target = open_browser)
    server_thr.start()
    browse_thr.start()



