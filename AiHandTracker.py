import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui as pag

#####
wCam, hCam = 640, 480
pTime = cTime = 0
#####

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
while True:
    # 1.Find LandMarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)


# 2 get the tip index and middle fingers
# 3 check which fingers are up
# 4Only INdex Finder:moving Mode
# 5COnvert coorordinates
# 6SMooth value
# 7 move mouse
# 8 both index and middle finder are up : clicking Mode
# 9 find dist
# 10 click mouse if dist short
# 11 frame ratee
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
# 12 display frame rate
    cv2.imshow("IMAGE", img)
    cv2.waitKey(1)
