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
abs_path =  '/root' #'/storage/emulated/0/Download' , 'C:/Users/ep/Desktop/epfs2/epfs2'
dir_list = []
file_list = []
video_list = []
audio_list = []
image_list = []
pdf_list = []

app = Flask(__name__, static_url_path='/static', static_folder = root_path, template_folder = root_path)

@app.route('/')
def index():
    files = os.listdir(abs_path)
    files.sort()
    
    dir_list.clear()
    file_list.clear()
    video_list.clear()
    audio_list.clear()
    image_list.clear()
    pdf_list.clear()
    
    for f in files:
        if os.path.isdir(f'{abs_path}/{f}'):
            dir_list.append(f)
        if os.path.isfile(f'{abs_path}/{f}'):
            filetype = os.path.splitext(f'{abs_path}/{f}')
            if  [x for x in ['jpg','png','bmp','jpeg','gif'] if x in filetype[1]]:
                image_list.append(f)
            elif  [x for x in ['mp3','wav'] if x in filetype[1]]:
                audio_list.append(f)
            elif  [x for x in ['mp4','mkv','mpg','mpeg','avi'] if x in filetype[1]]:
                video_list.append(f)
            elif  [x for x in ['pdf'] if x in filetype[1]]:
                pdf_list.append(f)
            else:
                file_list.append(f)
    return render_template('index.html', path="", dir_list=dir_list, file_list=file_list, pdf_list=pdf_list, image_list=image_list, audio_list=audio_list, video_list=video_list)
    
@app.route('/<path:path>')
def dir_listing(path):
    if os.path.isdir(f'{abs_path}/{path}'):
        files = os.listdir(os.path.join(abs_path,path))
        files.sort()
        dir_list.clear()
        file_list.clear()
        video_list.clear()
        audio_list.clear()
        image_list.clear()
        pdf_list.clear()
        
        for f in files:
            if os.path.isdir(f'{abs_path}/{path}/{f}'):
                dir_list.append(f)
            if os.path.isfile(f'{abs_path}/{path}/{f}'):
                filetype = os.path.splitext(f'{abs_path}/{path}/{f}')
                if  [x for x in ['jpg','png','bmp','jpeg','gif'] if x in filetype[1]]:
                    image_list.append(f)
                elif  [x for x in ['mp3','wav'] if x in filetype[1]]:
                    audio_list.append(f)
                elif  [x for x in ['mp4','mkv','mpg','mpeg','avi'] if x in filetype[1]]:
                    video_list.append(f)
                elif  [x for x in ['pdf'] if x in filetype[1]]:
                    pdf_list.append(f)
                else:
                    file_list.append(f)
        return render_template('index.html', path=path , dir_list=dir_list, file_list=file_list, pdf_list=pdf_list, image_list=image_list, audio_list=audio_list, video_list=video_list)
        
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

