from numpy.core.fromnumeric import resize
from ObjectDetection import ObjectDetection as ob
import glob, cv2, numpy as np

#global var to keep track of
show = False

def onTrackbarActivity(x):
    global show
    show = True
    pass

if __name__ == "__main__":
    # Get the filename from the command line
    files = glob.glob('images/*')
    files.sort()

    original = cv2.imread(files[0])
    
    image = ob(files[0], 0, 0, 0, 1, 1, 1)
    image1 = image.GetContours()

    rsize = 250
    
    #position on the screen where the windows start
    initialX = 50
    initialY = 50

    cv2.namedWindow('P-> Previous, N-> Next',cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('SelectHSV',cv2.WINDOW_AUTOSIZE)

    cv2.moveWindow('P-> Previous, N-> Next',initialX,initialY)
    cv2.moveWindow('SelectHSV',initialX + 2*(rsize + 5),initialY)

    #creating trackbars to get values for HSV
    cv2.createTrackbar('HMin','SelectHSV',0,180,onTrackbarActivity)
    cv2.createTrackbar('HMax','SelectHSV',0,180,onTrackbarActivity)
    cv2.createTrackbar('SMin','SelectHSV',0,255,onTrackbarActivity)
    cv2.createTrackbar('SMax','SelectHSV',0,255,onTrackbarActivity)
    cv2.createTrackbar('VMin','SelectHSV',0,255,onTrackbarActivity)
    cv2.createTrackbar('VMax','SelectHSV',0,255,onTrackbarActivity)

    i = 0

    cv2.imshow('SelectHSV',image1)

    while(1):
        cv2.imshow('P-> Previous, N-> Next' , image1)
        k = cv2.waitKey(1) & 0xFF

        if k == ord('n'):
            i += 1
            image = ob(files[i%len(files)], minHSV[0], minHSV[1], minHSV[2], maxHSV[0], maxHSV[1], maxHSV[2])
            image1 = image.GetContours()
            image1 = cv2.resize(image1,(rsize,rsize))
            show = True
             
        # check previous image in folder    
        elif k == ord('p'):
            i -= 1
            image = ob(files[i%len(files)], minHSV[0], minHSV[1], minHSV[2], maxHSV[0], maxHSV[1], maxHSV[2])
            image1 = image.GetContours()
            image1 = cv2.resize(image1,(rsize,rsize))
            show = True

        # Close all windows when 'esc' key is pressed
        elif k == 27:
            break

        if show: # If there is any event on the trackbar
            show = False

            HMin = cv2.getTrackbarPos('HMin','SelectHSV')
            SMin = cv2.getTrackbarPos('SMin','SelectHSV')
            VMin = cv2.getTrackbarPos('VMin','SelectHSV')
            HMax = cv2.getTrackbarPos('HMax','SelectHSV')
            SMax = cv2.getTrackbarPos('SMax','SelectHSV')
            VMax = cv2.getTrackbarPos('VMax','SelectHSV')
            minHSV = np.array([HMin, SMin, VMin])
            maxHSV = np.array([HMax, SMax, VMax])

            imageHSV = ob(files[i%len(files)], minHSV[0], minHSV[1], minHSV[2], maxHSV[0], maxHSV[1], maxHSV[2])
            imageHSV1 = imageHSV.GetResultHSV()
            imageHSV1 = cv2.resize(imageHSV1, (resize,resize))
            cv2.imshow('SelectHSV', imageHSV1)
