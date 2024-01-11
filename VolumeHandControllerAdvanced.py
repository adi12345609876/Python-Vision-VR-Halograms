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
colorVol = (255, 0, 0)
#####
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(detectionCon=0.7, maxHands=1)
while True:

    success, img = cap.read()
    # Find Hand
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=True)

    if len(lmList) != 0:
        # Filter Based on size
        area = (bbox[2]-bbox[0])*(bbox[3]-bbox[1])//100
        if 200 < area < 1000:
            # Find Dist between index and Thumb
            length, img, lineInfo = detector.findDistance(4, 8, img)

            # Convert volume
            volBar = np.interp(length, [minhanddist, maxhanddist], [400, 150])
            volPer = np.interp(length, [minhanddist, maxhanddist], [0, 100])
            # reduce resolution-Smoother
            smoothness = 10
            volPer = smoothness*round(volPer/smoothness)
            # check fingers up
            fingers = detector.fingersUp()
            # if pinky is down
            if fingers[4] == False:
                volume.SetMasterVolumeLevelScalar(volPer/100, None)
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                colorVol = (0, 255, 0)

            else:
                colorVol = (255, 0, 0)

    # Drawings
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)}%', (40, 450),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cVol = int(volume.GetMasterVolumeLevelScalar()*100)
    cv2.putText(img, f'Volume Set:{int(cVol)}%', (100, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                colorVol, 3)

    # Frame rate
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
