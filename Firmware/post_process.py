import cv2
import numpy as np

img = cv2.imread("image.jpg", 0)
img = cv2.GaussianBlur(img,(5,5),0)
#ret, thresh = cv2.threshold(img, 110,255,cv2.THRESH_BINARY_INV)
#ret, thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#            cv2.THRESH_BINARY,11,2)
#thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
#            cv2.THRESH_BINARY,11,2)
#print(ret)
#ret2,thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#print(ret2)
ret, thresh = cv2.threshold(img, 111, 255, cv2.THRESH_BINARY)
cv2.imwrite("thresh_image.jpg", thresh)
#print(np.mean(img))
