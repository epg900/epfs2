from flask import Flask, send_file, redirect,  render_template, request, Response
import os, time
import pyscreenshot as pss
from io import BytesIO

'''
#For running on android phone uncomment below lines an turn on hotspot on your android phone then start this script on pydroid
import socket, fcntl, struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

print(f" * Running on http://{get_ip_address(b'wlan0')}:5000")
'''
root_path = os.getcwd()
abs_path = '/home/ep' #'/storage/emulated/0/Download'

app = Flask(__name__, static_url_path='/static', static_folder = root_path, template_folder = root_path)

@app.route('/')
def index():
    files = os.listdir(abs_path)
    files.sort()
    return render_template('index.html', files=files)

@app.route('/<path:path>')
def dir_listing(path):
    if os.path.isdir(f'{abs_path}/{path}'):
        files = os.listdir(os.path.join(abs_path,path))
        files.sort()
        return render_template('index.html', path=path, files=files)
    else:
        return send_file(os.path.join(abs_path,path), conditional = True)

@app.route('/uploader' , methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for f in files:
            f.save(f'{abs_path}/{f.filename}')
        return redirect('/')

@app.route('/config' , methods = ['GET', 'POST'])
def config():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f'{abs_path}/{f.filename}')
    return redirect('/')

@app.route('/video' , methods = ['GET', 'POST'])
def video():
    if request.method == 'POST':
        f = request.files['file']
        if os.path.exists(f'{abs_path}/vid.mp4'):
            os.remove(f'{abs_path}/vid.mp4')
        f.save(f'{abs_path}/vid.mp4')
    return redirect('/vid.mp4')

app.run(host="0.0.0.0")

