#!/usr/bin/python

'''
This example illustrates how to use cv2.HoughCircles() function.

Usage:
    houghcircles.py [<image_name>]
    image argument defaults to board.jpg
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2
import cv2.cv

import sys

def main():
    try:
        fn = sys.argv[1]
    except IndexError:
        fn = 'board.jpg'

    #src = cv2.imread(cv2.samples.findFile(fn))
    src = cv2.imread(fn)
    img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img, 5)
    cimg = src.copy() # numpy function

    #circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT, 1, 4, np.array([]), 100, 30, 1, 30)
    circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT, 1, 10,20,30,40,300)

    if circles is not None: # Check if circles have been found and only then iterate over these and add them to the image
        a, b, c = circles.shape
        for i in range(b):
            cv2.circle(cimg, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 3, cv2.CV_AA)
            cv2.circle(cimg, (circles[0][i][0], circles[0][i][1]), 2, (0, 255, 0), 3, cv2.CV_AA)  # draw center of circle

        cv2.imshow("detected circles", cimg)

    cv2.imshow("source", src)
    cv2.waitKey(0)
    print('Done')


if __name__ == '__main__':
    print(__doc__)
    main()
    cv2.destroyAllWindows()
