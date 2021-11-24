import cv2
import numpy as np

class ObjectDetection:
    
    #Constructor
    def __init__(self, image, Hmin=0, Smin=0, Vmin=0, Hmax=1, Smax=1, Vmax=1):
        self.__image = cv2.imread(image)
        self.__minHSV = np.array([Hmin, Smin, Vmin])
        self.__maxHSV = np.array([Hmax, Smax, Vmax]) 

    #Convert in HSV
    def __ConvertInHSV(self):
        self.__imageHSV = cv2.cvtColor(self.__image, cv2.COLOR_BGR2HSV)
        maskHSV = cv2.inRange(self.__imageHSV, self.__minHSV, self.__maxHSV)
        self.__resultHSV = cv2.bitwise_and(self.__image, self.__image, mask=maskHSV)

    #Convert image in gray color
    def __PrepareForConversion(self):
        _image_gray = cv2.cvtColor(self.__resultHSV, cv2.COLOR_BGR2GRAY)
        self.__image_blur = cv2.GaussianBlur(_image_gray, (3,3), 0)

    #Convert image by Sobel
    def __ConvertBySobel(self):
        sobelx = cv2.Sobel(self.__image_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=3, scale=1, delta=0,  borderType=cv2.BORDER_DEFAULT)
        sobely = cv2.Sobel(self.__image_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3, scale=1, delta=0,  borderType=cv2.BORDER_DEFAULT)

        abs_sobelx = cv2.convertScaleAbs(sobelx)
        abs_sobely = cv2.convertScaleAbs(sobely)

        self.__sobel = cv2.addWeighted(abs_sobelx, 0.5, abs_sobely, 0.5, 0)

    #Finding contours on image
    def __FindContours(self):
        _, binary = cv2.threshold(self.__sobel, 30, 255, cv2.THRESH_BINARY)
        self.__contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    #Drawing contours
    def __DrawContours(self):
        self.__imageContours = self.__image.copy()
        return cv2.drawContours(self.__imageContours, self.__contours, -1, (0, 255, 0), 2, cv2.LINE_AA)
    

    #GetImageContours
    def GetContours(self):
        self.__ConvertInHSV()
        self.__PrepareForConversion()
        self.__ConvertBySobel()
        self.__FindContours()
        self.__DrawContours()
        return self.__imageContours

    def GetResultHSV(self):
        self.__ConvertInHSV()
        return self.__resultHSV

