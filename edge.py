#!/usr/bin/env python

'''
This sample demonstrates Canny edge detection.

Usage:
  edge.py [<video source>]

  Trackbars control edge thresholds.

'''

# Python 2/3 compatibility
from __future__ import print_function

import cv2
import cv2.cv
import numpy as np

# relative module
#import video

# built-in module
import sys


def main():
    try:
        fn = sys.argv[1]
    except:
        fn = 0

    def nothing(*arg):
        pass

    n = sys.argv[1]
    img = cv2.imread(fn)

    cv2.namedWindow('edge')
    cv2.createTrackbar('thrs1', 'edge', 2000, 5000, nothing)
    cv2.createTrackbar('thrs2', 'edge', 4000, 5000, nothing)

    while True:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret,thr = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)
        thr2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
        gray=thr;
        thrs1 = cv2.getTrackbarPos('thrs1', 'edge')
        thrs2 = cv2.getTrackbarPos('thrs2', 'edge')
        edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)
        vis = img.copy()
        vis = np.uint8(vis/2.)
        vis[edge != 0] = (0, 255, 0)
        cv2.imshow('edge', vis)
        ch = cv2.waitKey(5)
        if ch == 27:
            break

    print('Done')


if __name__ == '__main__':
    print(__doc__)
    main()
    cv2.destroyAllWindows()
