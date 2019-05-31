UNDER DEVELOPMENT!!!!  BACKUP FILES BEFORE USING.  

This program allows file encryption and decryption base on facial recognition.  Typed password must entered before
facial recognition can be performed.  Current passphrase is "password".  Will be changed soon.
Now the program requires both correct password to be entered and facial recognition to be performed to decrypt
the encrypted files.  The passwords are not stored in the directory.   They are combined with salt phrases to protect
against rainbow tables.

Use the following command to open the GUI:
python facial_gui.py 'device number'

find webcam device with ls /dev/video*
for instance, if your webcam is /dev/video4, use this command.

python facial_gui.py 4

First, a image must be selected to be used as the verification key.  
This is done by seleting the command from the Tools menu.
The image recognition compares the video frame to
this image to determine if the faces match.  

Second, the user must be within the Green Box to take a snapshot.  The on-screen text notifies when a face has been detected
and the user can press the Snapshot button to grab the frame at this time.  The debug terminal will show if there was 
a positive match. If a positive match was determine, files can be encrypted or decrypted.


The facial recognition feature is another github project:  https://github.com/ageitgey/face_recognition

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
use salt and pepper rather than only salt.
perhaps use verification image as password phase.
Allow encyption key to be reset and re-encrypt encrypted files with new encryption key.
Create Functions to encrypt and decrypt all files in directory.
Remove original files after encrypted.



