import cv2 as cv
import numpy as np
import sys


def detect_eyes(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def detect_face(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv.rectangle(img, (x1, y1), (x2, y2), color, 2)


def gen_face(img, gray, face_cascade):
    rects_face = detect_eyes(gray, face_cascade)
    r = rects_face
    ex_face = img[r[0][1]:r[0][3], r[0][0]:r[0][2]]
    return ex_face, r, rects_face


face_cascade = cv.CascadeClassifier('/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
eyes_cascade = cv.CascadeClassifier('/usr/local/share/opencv4/haarcascades/haarcascade_eye.xml')
fn = sys.argv[1]
img = cv.imread(fn)

# 1.  Detect Face and Extract ROI.
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = cv.equalizeHist(gray)
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
    gray_face = cv.cvtColor(vis2, cv.COLOR_BGR2GRAY)
    gray_face = cv.equalizeHist(gray_face)

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
            cv.imshow("Lena", vis1)
            cv.imshow("Lena Face", vis2)
            cv.imshow("Lena Eye1", ex_eye1)
            cv.imshow("Lena Eye2", ex_eye2)
            cv.waitKey(0)
        # One eye
        elif s1 == 1:
            ex_eye1 = vis2[r[0][1]:r[0][3], r[0][0]:r[0][2]]
            print("Face and One Eye Detected.");
            draw_rects(vis1, rects_face, (0, 255, 0))
            draw_rects(vis2, rects_eyes, (0, 255, 0))
            cv.imshow("Lena", vis1)
            cv.imshow("Lena Face", vis2)
            cv.imshow("Lena Eye1", ex_eye1)
            cv.waitKey(0)
        # No eyes.
        else:
            print("Error. Face, But No Eyes Detected.")

    # Face and No eyes.
    except:
        print("Face But No Eyes Detected.");
        draw_rects(vis1, rects_face, (0, 255, 0))
        cv.imshow("Lena", vis1)
        cv.imshow("Lena Face", vis2)
        cv.waitKey(0)

else:
    # No Face, But Eyes.
    gray_face = cv.cvtColor(vis1, cv.COLOR_BGR2GRAY)
    gray_face = cv.equalizeHist(gray_face)
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
            cv.imshow("Lena", vis1)
            cv.imshow("Lena Eye1", ex_eye1)
            cv.imshow("Lena Eye2", ex_eye2)
            cv.waitKey(0)
        # One eye
        elif s1 == 1:
            ex_eye1 = vis1[r[0][1]:r[0][3], r[0][0]:r[0][2]]
            print("No Face and One Eye Detected.");
            draw_rects(vis1, rects_eyes, (0, 255, 0))
            cv.imshow("Lena", vis1)
            cv.imshow("Lena Eye1", ex_eye1)
            cv.waitKey(0)
        # No eyes.
        else:
            print("No Face and No Eyes Detected.")
    # No Eyes and No Face
    except:
        print("Nothing detected.");
