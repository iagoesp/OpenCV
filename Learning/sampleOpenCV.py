import cv2
import numpy as np

img = cv2.imread('lenna.jpg', 1)

M = cv2.getRotationMatrix2D((cols/2, rows/2), 0, 1)
dst = cv2.warpAffine(img,M,(cols,rows))

cv2.imshow('img',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()