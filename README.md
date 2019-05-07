#Note, this was build for aarch64 architecture on Lenovo C330 chromebook running Linux Crouton.  The Mediatek CPU architecture
#Is rare and opencv needed to be cross-compiled for the architecture to operate.
#OpenCV4 was built from source for cross-compilation, After this, I was able to install opencv using apt-get. 
#I initially used Python3 and pip3.
#OpenCV only worked on this architecture with Pip2 and Python2.7.  
#I had to set these as my default configurations.  
#After instsalling with apt-get and resetting the defaults configurations, I was able to import cv2 in Python.
#And now the OpenCV commands work as expected in Python, but the tests and samples do not work from the CLI.

Currently, the program can run eye_extract.py from the Ubuntu Terminal command line.  
This loads a photo, detects eyes and separates them from the rest of the image.

Next, I need to compare the extracted images to a trained model and determine if this matches the same eyes or not.   
If the eyes match, then encrypt/decrypt a file.

How to accomplish this?
A dougman algorithm can be used to extract the Iris from the photos.
Use this algorithm to generate a set of features for each image.
Then classify these features for each individual in the training data.
If the new photo matches the expected class (my photo) from the training set, then run the file encryption function.



