import cv2
import time
import os
import HandTrackingModule as htm
import numpy as np
wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = lfps = fps = Ffps = xp = yp = 0
# Folder
folderPath = "Paintboard"
myList = os.listdir(folderPath)
overLayList = []
for imgP in myList:
    image = cv2.imread(f'{folderPath}/{imgP}')
    overLayList.append(image)
# BRGcolors = {
#     "orange": (255, 100, 0),
#     "blue": (0, 255, 255),
#     "green": (0, 255, 0),
#     "black": (0, 0, 0),
#     "red": (0, 0, 255),
#     "yellow": (255, 255, 0),
#     "purple": (255, 0, 255),
#     "pink": (255, 0, 150)
# }
drawColor = (0, 0, 255)
header = overLayList[0]
###
brushThickness = 15
eraserThickness = 150

###
imgCanvas = np.zeros((720, 1280, 3), np.uint8)
# HandDetector
detector = htm.handDetector(detectionCon=0.85)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
   # show board

    # Hand draw
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # tip of index and middle finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

    # check which finger up
    fingers = detector.fingersUp()
    if len(fingers) != 0:
        # selection mode - 2 finger
        if fingers[1] and fingers[2]:
            xp = yp = 0
            # checking click
            if y1 < 140:

                if 250 < x1 < 350:
                    header = overLayList[0]
                    drawColor = (0, 0, 255)
                elif 450 < x1 < 650:
                    header = overLayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overLayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = overLayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1-25), (x2, y2+25),
                          drawColor, cv2.FILLED)
        # Drawing mode - index finger up
        if fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 25, drawColor, cv2.FILLED)
            print("Draawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y2
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1),
                         drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1),
                         drawColor, brushThickness)

            xp, yp = x1, y1

    # framerate
    lfps = fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
   # print(int(lfps), int(fps), int(lfps)-int(fps))
    if abs(int(lfps)-int(fps)) > 25:
        Ffps = fps

    cv2.putText(img, f'FPS:{int(Ffps)}', (50, 50),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    # Setting the header and img showing
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)
    img[0:125, 0:1280] = header
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Video", img)
    # cv2.imshow("Canvas", imgCanvas)
    # cv2.imshow("Inv", imgInv)

    cv2.waitKey(1)
