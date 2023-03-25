import cv2
from cv2 import aruco
from object_detector import *
import numpy as np


dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
parameters =  cv2.aruco.DetectorParameters()
# detector = cv2.aruco.ArucoDetector(dictionary, parameters)
detector = HomogeneousBgDetector()


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
while True:
    _, img = cap.read() 

    # get aruco marker
    corners, _, _ = cv2.aruco.detectMarkers(img,dictionary,parameters=parameters)
    print(corners)
    if corners:
        int_corners = np.int0(corners)
        cv2.polylines(img,int_corners, True, (0,255,0), 5)

        aruco_parimeter = cv2.arcLength(corners[0], True)

        # convert pixel to cm ratio
        pixel_cm_ratio = aruco_parimeter / 20
        print(pixel_cm_ratio)



        contours = detector.detect_objects(img)

        for cnt in contours:
            # get rect
            rect = cv2.minAreaRect(cnt)
            (x,y), (w,h), angle = rect

            obj_w = w / pixel_cm_ratio
            obj_h = h / pixel_cm_ratio


            # display rectangle
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            
            cv2.circle(img, (int(x),int(y)), 5, (0,0,225), -1)
            cv2.polylines(img, [box], True, (255,9,0), 2)
            cv2.putText(img, "Width {} cm".format(round(obj_w,1)), (int(x - 100), int(y - 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100,200,0), 2)
            cv2.putText(img, "High {} cm".format(round(obj_h,1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100,200,0), 2)



    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()