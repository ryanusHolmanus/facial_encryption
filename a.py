import cv2 as cv
import numpy as np
import sys

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv.rectangle(img, (x1, y1), (x2, y2), color, 2)

#cascade = cv.CascadeClassifier('/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
cascade = cv.CascadeClassifier('/usr/local/share/opencv4/haarcascades/haarcascade_eye.xml')
fn = sys.argv[1]
img=cv.imread(fn)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = cv.equalizeHist(gray)
rects = detect(gray, cascade)
vis = img.copy()
draw_rects(vis, rects, (0, 255, 0))

cv.imshow("Lena", vis)
cv.waitKey(0)
