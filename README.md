# DISCLAIMER

#### ConTroll is for education/research purposes only. The author takes NO responsibility and/or liability for how you choose to use any of the tools/source code/any files provided. The author and anyone affiliated with will not be liable for any losses and/or damages in connection with use of ANY files provided with ConTroll. By using ConTroll or any files included, you understand that you are AGREEING TO USE AT YOUR OWN RISK. Once again ConTroll and ALL files included are for EDUCATION and/or RESEARCH purposes ONLY. ConTroll is ONLY intended to be used on your own pentesting labs, or with explicit consent from the owner of the property being tested.

# ConTroll - Remote Access Trojan (RAT)

Created a remote access trojan that will establish administrative control over any machine it compromises.

![alt text](img/1.PNG)

# Features

1. Lock Victim's screen.
2. Create a custom popup box.
3. Auto recconnect to Server.
4. Grab files from the victim's machine.
5. Get information about victim's machine.
6. Steal saved passwords stored in chrome.
7. Activate a system’s webcam and record video.
8. Kill any process running on victim's machine.
9. Monitoring user behavior through keylogger capabilities (Keystrokes and Screenshots).

# Requirements

1. opencv
2. numpy
3. pyhook
4. pyinstaller

# Usage

1. Install requirements.txt

2. Set ip_address. The ip_address is taken from the server's network

3. Use pyinstaller to build the client binary
```
python pyinstaller.py --onefile --windowed --icon=icon.ico client.pyw
```

4. Run the server
```
python server.py
```

5. Wait for the client to connect

# ToDo

1. Clear the System, Security, and Application logs
2. Encrypt communication between server and client
3. Edit the accessed, created, and modified properties of files
4. Enable/Disable services such as RDP,UAC, and Windows Defender
