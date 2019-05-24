UNDER DEVELOPMENT!!!!

The program currently opens the PC webcam and takes a snapshot of the user.  If the snapshot matches the facial image specified from a separate file, then the input file will be encrypted and decrypted to a separate file.

This is temporary usage and will be changed soon.....
This example uses facial recognition to encrypt and decrypt file. 
I have not finished the iris recognition function.
The facial recognition feature is another github project:  https://github.com/ageitgey/face_recognition.
Two lines of code will most likely need to be change:
1.  cap = cv2.VideoCapture(4)  --> will likely be a different device number
2.  known_image = face_recognition.load_image_file("/home/rhh/progs/rhh_iris/me.jpg")
    known image is the image to compare the snapshot against to determine if the person in the video is the desired person....
    This photo is not included in the project files, but should be a facial image of the user.
Also, the encryption key is extremely basic....

python eye_extract.py {input image file} {output encrypted filename} {output decrypted filename}
python eye_extract.py lena.jpg test1.jpg test2.jpg

On success, test1.jpg is an encrypted image file and test2.jpg is test1.jpg after being decrypted to the original file (lena.jpg)

NO DAUGMAN ALGORITHM IMPLEMENTED YET

BIGGEST DIFFICULTY IS FINDING DAUGMAN PYTHON SCRIPT FOR aarch64 architecture. 

Note, this was build for aarch64 architecture on Lenovo C330 chromebook running Linux Crouton.  The Mediatek CPU architecture
Is rare and opencv needed to be cross-compiled for the architecture to operate.
OpenCV4 was built from source for cross-compilation, After this, I was able to install opencv using apt-get. 
I initially used Python3 and pip3.
OpenCV only worked on this architecture with Pip2 and Python2.7.  
I had to set these as my default configurations.  
After instsalling with apt-get and resetting the defaults configurations, I was able to import cv2 in Python.
And now the OpenCV commands work as expected in Python, but the tests and samples do not work from the CLI.

Currently, the program can run eye_extract.py from the Ubuntu Terminal command line. 
There is additional function that is suppressed in the script by default, but that works. 
This loads a photo, detects eyes and separates them from the rest of the image.
This is to be used for iris recognition encryption rather than facial recognition encryption.

Next, I need to compare the extracted images to a trained model and determine if this matches the same eyes or not.   
If the eyes match, then encrypt/decrypt a file.

How to accomplish this?
A dougman algorithm can be used to extract the Iris from the photos.
Use this algorithm to generate a set of features for each image.
Then classify these features for each individual in the training data.
If the new photo matches the expected class (my photo) from the training set, then run the file encryption function.



