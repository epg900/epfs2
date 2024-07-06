from flask import Flask, send_file, redirect,  render_template, request
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

abs_path = os.getcwd() #'/storage/emulated/0/Download'

app = Flask(__name__, static_url_path='/static', static_folder = abs_path, template_folder = abs_path)

@app.route('/')
def index():
    return redirect('/upload')

@app.route('/upload')
def dir_listing():
    files = os.listdir(os.path.join(abs_path , "upload"))
    files.sort()
    return render_template('index.html', files=files)

@app.route('/uploader' , methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for f in files:
            f.save(f'{abs_path}/upload/{f.filename}')
        return redirect('/upload')

@app.route('/config' , methods = ['GET', 'POST'])
def config():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f'{abs_path}/upload/{f.filename}')
    return redirect('/')

@app.route('/video' , methods = ['GET', 'POST'])
def video():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f'{abs_path}/upload/vid.mp4')
        return redirect('/p/vid.mp4')

@app.route('/p/<filename>')
def play(filename):
	return send_file(f'{abs_path}/upload/{filename}', conditional = True)

@app.route('/screen')
def screen():
    return render_template('screen.html')

@app.route('/screen.png')
def screenshot():
    img_buffer = BytesIO()
    pss.grab().save(img_buffer, 'PNG', quality=50)
    img_buffer.seek(0)
    return send_file(img_buffer, mimetype='image/png')


app.run(host="0.0.0.0")
