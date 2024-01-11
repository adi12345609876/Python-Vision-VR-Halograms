import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui as pag
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# https://developers.google.com/mediapipe/solutions/vision/hand_landmarker#:~:text=The%20hand%20landmark%20model%20bundle,models%20imposed%20over%20various%20backgrounds.
#####
wCam, hCam = 640, 480
pTime = cTime = 0
#####
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#####
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()  # Volume range :65 - 0

minVol = volRange[0]
maxVol = volRange[1]
minhanddist = 20
maxhanddist = 150
vol = 0
volBar = 400
volPer = 0
#####
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(detectionCon=0.7)
while True:

    success, img = cap.read()
    # Find Hand
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=True)

    if len(lmList) != 0:
        # Filter Based on size
        area = (bbox[2]-bbox[0])*(bbox[3]-bbox[1])//100
        # Find Dist between index and Thumb
        # Convert volume
        # reduce resolution-Smoother
        # check fingers up
        # if pinky is down
        # Drawings
        # Frame rate
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)  # hand range:20-250
        ###
        # hand range --> Vol range
        vol = np.interp(length, [minhanddist, maxhanddist], [minVol, maxVol])
        volBar = np.interp(length, [minhanddist, maxhanddist], [400, 150])
        volPer = np.interp(length, [minhanddist, maxhanddist], [0, 100])

        ###

        volume.SetMasterVolumeLevel(vol, None)
        # print(length)
        if length <= 25:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # else:NO hands in the screen
    # vol bar
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # fps2 = fps
    # if fps2-fps > 10:
    #     cv2.putText(img, f'FPS:{int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    #                 (255, 0, 0), 3)
# 12 display frame rate
    cv2.imshow("IMAGE", img)
    cv2.waitKey(1)
