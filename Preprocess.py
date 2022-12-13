import cv2 as cv
import numpy as np
from skimage.morphology import skeletonize
import pickle

def preprocess(img):
    cv.imwrite('steps/01.png',img)
    img=cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,13,7)
    cv.imwrite('steps/02.png',img)
    img = cv.medianBlur(img,3)
    cv.imwrite('steps/03.png',img)
    ret,img = cv.threshold(img,127,255,cv.THRESH_BINARY)
    cv.imwrite('steps/04.png',img)
    img=255-img
    cv.imwrite('steps/05.png',img)
    img = skeletonize(img, method='lee')
    cv.imwrite('steps/06.png',img)
    cv.waitKey()
    contours=contour_detect(img,2)
    lines=[]
    black_image = np.full((img.shape[0], img.shape[1]),0.)
    filled_con=cv.drawContours(black_image,contours,-1,(1,255,0),1)
    cv.imwrite('steps/07.png',filled_con)
    cv.waitKey() 

    for i in range(len(contours)):
        contours[i]=contours[i][:,0]
    lines=contours
    return lines


def contour_detect(img,min_length):
    ret,thresh=cv.threshold(img,0.6,1,0)
    contours,hierachy=cv.findContours(img,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
    contours_filtered=[]
    for i in contours:
      length=cv.arcLength(i,True)
      if length>min_length:
        contours_filtered+=[i]
    return contours_filtered

 

def detect_lines(img_path):
    img= cv.imread(img_path,0)
    lines=preprocess(img)

    return lines,img.shape

if __name__=='__main__':
    lines,shape=detect_lines('samples/01.jpg')
