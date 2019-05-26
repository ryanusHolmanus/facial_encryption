UNDER DEVELOPMENT!!!!  BACKUP FILES BEFORE USING.  

This program allows file encryption and decryption base on facial recognition.

Use the following command to open the GUI:
python iris_gui.py

First, a image must be selected to be used as the verification key.  
This is done by seleting the command from the Tools menu.
The image recognition compares the video frame to
this image to determine if the faces match.  

Second, the user must be within the Green Box to take a snapshot.  The on-screen text notifies when a face has been detected
and the user can press the Snapshot button to grab the frame at this time.  The debug terminal will show if there was 
a positive match. If a positive match was determine, files can be encrypted or decrypted.

Only works in single session.  The encryption and decryption key is regenerated each time and encrypted files from a previous
session cannot be decrypted in the next session.

Moved from command line to GUI.  
Also only support facial recognition, not iris recognition.

The facial recognition feature is another github project:  https://github.com/ageitgey/face_recognition

Two lines of code will most likely need to be change:
1.  cap = cv2.VideoCapture(4)  --> will likely be a different device number
    Should make user select device if default is faulty.  And set default device.

BIGGEST DIFFICULTY IS FINDING DAUGMAN PYTHON SCRIPT FOR aarch64 architecture. 

Note, this was build for aarch64 architecture on Lenovo C330 chromebook running Linux Crouton.  The Mediatek CPU architecture
Is rare and opencv needed to be cross-compiled for the architecture to operate.
OpenCV4 was built from source for cross-compilation, After this, I was able to install opencv using apt-get. 
I initially used Python3 and pip3.
OpenCV only worked on this architecture with Pip2 and Python2.7.  
I had to set these as my default configurations.  
After installing with apt-get and resetting the defaults configurations, I was able to import cv2 in Python.
And now the OpenCV commands work as expected in Python, but the tests and samples do not work from the CLI.

To Do:
Menu option to Set default video device path.  Allow to be saved to subsequent sessions.
Reconfigure encryption key to remain the same for subsequent sessions.
Allow encyption key to be reset and re-encrypt encrypted files with new encryption key.
Create Functions to encrypt and decrypt all files in directory.
Remove original files after encrypted.

