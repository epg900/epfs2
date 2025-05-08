from flask import Flask, send_file, redirect,  render_template, request
import os

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
abs_path =  '/storage/emulated/0/Download' #'/root'  , 'C:/Users/e.pishvaz/Desktop/epfs2'
varlist = ['folder','image','audio','video','pdf','file']

def retlist(path=""):
    all_list = []
    for i in range(0,7):
        all_list.append([])

    new_path = os.path.join(abs_path,path)    
    files = os.listdir(os.path.join(abs_path,path))
        
    files.sort()
    for f in files:
        if os.path.isdir(os.path.join(new_path,f)):
            all_list[0].append(f)
        if os.path.isfile(os.path.join(new_path,f)):
            filetype = os.path.splitext(os.path.join(new_path,f))
            if  [x for x in ['jpg','png','bmp','jpeg','gif'] if x in filetype[1]]:
                all_list[1].append(f)
            elif  [x for x in ['mp3','wav'] if x in filetype[1]]:
                all_list[2].append(f)
            elif  [x for x in ['mp4','mkv','mpg','mpeg','avi'] if x in filetype[1]]:
                all_list[3].append(f)
            elif  [x for x in ['pdf'] if x in filetype[1]]:
                all_list[4].append(f)
            else:
                all_list[5].append(f)
    return all_list


    
app = Flask(__name__, static_url_path='/static', static_folder = root_path, template_folder = root_path)

@app.route('/')
def index():
    lst = retlist()
    return render_template('index.html', path = "", all_list = lst , varlist = varlist )
    
@app.route('/<path:path>')
def dir_listing(path):
    if os.path.isdir(f'{abs_path}/{path}'):        
        lst = retlist(path)
        return render_template('index.html', path=path , all_list = lst , varlist = varlist  )
        
    else:
        return send_file(os.path.join(abs_path,path), conditional = True)
    return redirect('/')

'''
import pyotp, glob

@app.route('/rm/<code>/<path:path>')
def rm_file(code,path):
    otp_chk = pyotp.TOTP('')
    if otp_chk.now() == code:
        files = glob.glob(f'{abs_path}/{path}')
        for file in files:
            os.remove(file)        
    return redirect('/')
'''

@app.route('/uploader' , methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for f in files:
            f.save(f'{abs_path}/{f.filename}')
    return redirect('/')

app.run(host="0.0.0.0")

