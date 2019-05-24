#Example Usage
#This is temporary usage and will be changed soon.....
#This example uses facial recognition to encrypt and decrypt file. I have not finished the iris recognition function.
#Two lines of code will most likely need to be change:
#1.  cap = cv2.VideoCapture(4)  --> will likely be a different device number
#2.  known_image = face_recognition.load_image_file("/home/rhh/progs/rhh_iris/moi/n_40.png")
    #known image is the image to compare the snapshot against to determine if the person in the video is the desired person....
#Also, the encryption key is extremely basic....

# python eye_extract.py {input image file} {output encrypted filename} {output decrypted filename}
# python eye_exctract.py lena.jpg test1.jpg test2.jpg

#On success, test1.jpg is an encrypted image file and test2.jpg is test1.jpg after being decrypted to the original file (lena.jpg)

#Note, this was build for aarch64 architecture on Lenovo C330 chromebook running Linux Crouton.  The Mediatek CPU architecture
#Is rare and opencv needed to be cross-compiled for the architecture to operate.
#OpenCV4 was built from source for cross-compilation, After this, I was able to install opencv using apt-get.
#I initially used Python3 and pip3.
#OpenCV only worked on this architecture with Pip2 and Python2.7.
#I had to set these as my default configurations.
#After installing with apt-get and resetting the defaults configurations, I was able to import cv2 in Python.
#And now the OpenCV commands work as expected in Python, but the tests and samples do not work from the CLI.
#useful guide: https://nitratine.net/blog/post/encryption-and-decryption-in-python/#encrypting-and-decrypting-files

from __future__ import division
import cv2
import cv2.cv
import numpy as np
import sys
#https://github.com/ageitgey/face_recognition
import face_recognition
from cryptography.fernet import Fernet

key = Fernet.generate_key()
#key = b'0xAA'
fernet = Fernet(key)

def akey():
	file = open('key.key', 'wb')
	file.write(key) # The key is type bytes still
	file.close()
	return

def dec_file():
    with open(sys.argv[2], 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.decrypt(data)
    with open(sys.argv[3], 'wb') as f:
        f.write(encrypted)
    return

def enc_file(data):
    encr=fernet.encrypt(data)
    outf=sys.argv[2]
    with open(outf,'wb') as oof:
            oof.write(encr)
    return


def load_input(fn):
    #with open(fn) as ain:
    #    for item in ain:
    #        print(item);
    with open(fn,'rb') as ain:
        data=ain.read()
    return data

def fr_enc():
    akey()
    fn = sys.argv[1]
    print("loading input file")
    data=load_input(fn)
    print('encrypting file.')
    enc_file(data)
    print('decrypting file')
    dec_file()
    print('finished')
    return

def detect_eyes(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def detect_face(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)


def gen_face(img, gray, face_cascade):
    rects_face = detect_eyes(gray, face_cascade)
    r = rects_face
    ex_face = img[r[0][1]:r[0][3], r[0][0]:r[0][2]]
    return ex_face, r, rects_face

def find_circles(src):
    img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img, 5)
    cimg = src.copy()  # numpy function

    circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT, 1, 10, np.array([]), 100, 30, 1, 30)
    print("Circle array size")
    print(circles.shape)

    if circles is not None:  # Check if circles have been found and only then iterate over these and add them to the image
        a, b, c = circles.shape
        for i in range(b):
            cv2.circle(cimg, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 3, cv2.CV_AA)
            cv2.circle(cimg, (circles[0][i][0], circles[0][i][1]), 2, (0, 255, 0), 3,
                       cv2.CV_AA)  # draw center of circle
    return cimg

def fr3():
    # to do:
    # make ROI in video feed.
    # if face detected... print label in video and allow snapshot with keypress
    # when snapshot is make compare to my encoded image to determine if it is me....
    # then encrypt/decrypt file upon success....
    face_cascade = cv2.CascadeClassifier('/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(4)
    b=0
    while (True):
        # Capture frame-by-frame
        if (b==0):
            eva, frame = cap.read()
            iframe=frame.copy();
        else:
            eva==False
        #width, height = cv2.GetSize(frame)
        #width, height = frame.shape[:2]
        height, width = frame.shape[:2]
        if eva is True:
            # Our operations on the frame come here
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #make ROI in frame
            cv2.rectangle(frame, (int(5*width/16), int(1/8*height)), (int(11/16*width), int(7/8*height)), (0, 255, 0), 2)
            roi_frame=frame[int(1/8*height):int(7/8*height),int(5*width/16):int(11/16*width)]
            #print(roi_frame.shape[:2])
            #use haarcascade to detected face in rectangle....
            # if face detected... print Face Dected on screeen.....
            roi_gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
            roi_gray = cv2.equalizeHist(roi_gray)
            roi_vis1 = roi_frame.copy()
            try:
                ex_face, r, rects_face = gen_face(frame, roi_gray, face_cascade)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'Face Detected.  Press s to take snapshot.', (10, int(1/16*height)), font, .75, (255, 255, 255), 2, cv2.CV_AA)
                #print("Face Detected.");
                #take snapshot with keypress
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    frame=iframe.copy();
                    b=1
                    #Now compare the snapshot to a previous image of me and determine if it is the same person.
                    known_image = face_recognition.load_image_file("/home/rhh/progs/rhh_iris/me.jpg")
                    unknown_image = frame.copy();
                    rhh_encoding = face_recognition.face_encodings(known_image)[0]
                    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
                    results = face_recognition.compare_faces([rhh_encoding], unknown_encoding)
                    print(results)
                    print(results[0])
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    if results[0] == True:
                        print("TrueTrue")
                        cv2.putText(frame, 'Snapshot Taken.  This is Ryan.', (10, int(15 / 16 * height)), font, .75, (255, 255, 255), 2, cv2.CV_AA)
                        fr_enc();
                    else:
                        print("FalseFalse")
                        cv2.putText(frame, 'Snapshot Taken.  This is not Ryan.', (10, int(15 / 16 * height)), font, .75, (255, 255, 255), 2, cv2.CV_AA)
            except:
                #print("No Face Detected.");
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'No Face Detected.', (10, int(1/16*height)), font, .75, (255, 255, 255), 2, cv2.CV_AA)


        else:
            continue
        # Display the resulting frame
        cv2.imshow('frame', frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return

def fr4():
    face_cascade = cv2.CascadeClassifier('/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
    eyes_cascade = cv2.CascadeClassifier('/usr/local/share/opencv4/haarcascades/haarcascade_eye.xml')
    fn = sys.argv[1]
    img = cv2.imread(fn)

    # 1.  Detect Face and Extract ROI.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    vis1 = img.copy()
    a = 0;

    try:
        ex_face, r, rects_face = gen_face(img, gray, face_cascade)
        print("Face Detected.");
        vis2 = ex_face.copy()
        a = 1;
    except:
        print("error.");
    if a == 0:
        print("No Face Detected.");

    # 2.  Use Face ROI and detect eyes, then extract ROI
    # Need to account for multiple Faces??  Can Just throw error.
    if a == 1:
        gray_face = cv2.cvtColor(vis2, cv2.COLOR_BGR2GRAY)
        gray_face = cv2.equalizeHist(gray_face)

        # Face and eyes.
        try:
            rects_eyes = detect_eyes(gray_face, eyes_cascade)
            r = rects_eyes
            s1, s2 = r.shape  # Wont work if less than two eyes detected.
            # More than two eyes.
            if s1 > 2:
                print("Error. More than two eyes detected.");
            # Two eyes
            elif s1 == 2:
                # Need iterative for more than two eyes.
                ex_eye1 = vis2[r[0][1]:r[0][3], r[0][0]:r[0][2]]
                ex_eye2 = vis2[r[1][1]:r[1][3], r[1][0]:r[1][2]]
                print("Face and Two Eyes Detected");
                draw_rects(vis1, rects_face, (0, 255, 0))
                draw_rects(vis2, rects_eyes, (0, 255, 0))
                # resize extracted eyes to make larger
                ex_eye1 = cv2.resize(ex_eye1, (300, 300), interpolation=cv2.INTER_AREA)
                ex_eye2 = cv2.resize(ex_eye2, (300, 300), interpolation=cv2.INTER_AREA)
                # find circles in extracted eye image and draw
                # cimg1=find_circles(ex_eye1)
                # cimg2=find_circles(ex_eye2)
                cv2.imshow("Lena", vis1)
                cv2.imwrite("vis1.png", vis1)
                cv2.imshow("Lena Face", vis2)
                cv2.imwrite("vis2.png", vis2)
                cv2.imshow("Lena Eye1", ex_eye1)
                cv2.imwrite("ex_eye1.png", ex_eye1)
                cv2.imshow("Lena Eye2", ex_eye2)
                cv2.imwrite("ex_eye2.png", ex_eye2)
                # cv2.imshow("ex_eye1 circles", cimg1)
                # cv2.imshow("ex_eye2_circles", cimg2)
                cv2.waitKey(0)
            # One eye
            elif s1 == 1:
                ex_eye1 = vis2[r[0][1]:r[0][3], r[0][0]:r[0][2]]
                print("Face and One Eye Detected.");
                draw_rects(vis1, rects_face, (0, 255, 0))
                draw_rects(vis2, rects_eyes, (0, 255, 0))
                ex_eye1 = cv2.resize(ex_eye1, (300, 300), interpolation=cv2.INTER_AREA)
                cv2.imshow("Lena", vis1)
                cv2.imwrite("vis1.png", vis1)
                cv2.imshow("Lena Face", vis2)
                cv2.imwrite("vis2.png", vis2)
                cv2.imshow("Lena Eye1", ex_eye1)
                cv2.imwrite("ex_eye1.png", ex_eye1)
                cv2.waitKey(0)
            # No eyes.
            else:
                print("Error. Face, But No Eyes Detected.")

        # Face and No eyes.
        except:
            print("Face But No Eyes Detected.");
            draw_rects(vis1, rects_face, (0, 255, 0))
            cv2.imshow("Lena", vis1)
            cv2.imshow("Lena Face", vis2)
            cv2.waitKey(0)

    else:
        # No Face, But Eyes.
        gray_face = cv2.cvtColor(vis1, cv2.COLOR_BGR2GRAY)
        gray_face = cv2.equalizeHist(gray_face)
        try:
            rects_eyes = detect_eyes(gray_face, eyes_cascade)
            r = rects_eyes
            s1, s2 = r.shape  # Wont work if less than two eyes detected.
            # More than two eyes.
            if s1 > 2:
                print("More than two eyes detected.");
            # Two eyes.
            elif s1 == 2:
                ex_eye1 = vis1[r[0][1]:r[0][3], r[0][0]:r[0][2]]
                ex_eye2 = vis1[r[1][1]:r[1][3], r[1][0]:r[1][2]]
                print("No Face and Two Eyes Detected");
                draw_rects(vis1, rects_eyes, (0, 255, 0))
                cv2.imshow("Lena", vis1)
                cv2.imshow("Lena Eye1", ex_eye1)
                cv2.imshow("Lena Eye2", ex_eye2)
                cv2.waitKey(0)
            # One eye
            elif s1 == 1:
                ex_eye1 = vis1[r[0][1]:r[0][3], r[0][0]:r[0][2]]
                print("No Face and One Eye Detected.");
                draw_rects(vis1, rects_eyes, (0, 255, 0))
                cv2.imshow("Lena", vis1)
                cv2.imshow("Lena Eye1", ex_eye1)
                cv2.waitKey(0)
            # No eyes.
            else:
                print("No Face and No Eyes Detected.")
        # No Eyes and No Face
        except:
            print("Nothing detected.");
    return

def main():
    #fr1()
    #fr2()
    fr3()
    #fr4()
    return

main();

