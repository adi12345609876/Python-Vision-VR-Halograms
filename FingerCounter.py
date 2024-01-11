import cv2
import time
import os
import HandTrackingModule as htm
wCam, hCam = 680, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
# get finger images folder
folderPath = "FingerImages"
myList = os.listdir(folderPath)

overlay = []
for imgP in myList:
    image = cv2.imread(f'{folderPath}/{imgP}')
    overlay.append(image)

pTime, lfps, fps, Ffps = 0, 0, 0, 0
# HandDetector
detector = htm.handDetector(detectionCon=0.7)
TipIds = [4, 8, 12, 16, 20]
while True:
    success, img = cap.read()
    # Hand draw
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # open or closed finger =    check tip less than lower pint
    if len(lmList) != 0:
        # if lmList[8][2] < lmList[6][2]:
        #     print("Index finger open")
        fingers = []
        if lmList[TipIds[0]][1] > lmList[TipIds[0]-1][2]:
            fingers.append(1)
            # print(TipIds[id],"open")
        else:
            fingers.append(0)

        for id in range(1, 5):
            if lmList[TipIds[id]][2] < lmList[TipIds[id]-2][2]:
                fingers.append(1)
                # print(TipIds[id],"open")
            else:
                fingers.append(0)
        # print(fingers)
        totalFinger = fingers.count(1)

        # showing picture
        h, w, c = overlay[totalFinger-1].shape
        img[0:h, 0:w] = overlay[totalFinger-1]
        # showing count
        cv2.putText(img, f'Count:{totalFinger}', (400, 100),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    # cv2 display and framerate
    lfps = fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
   # print(int(lfps), int(fps), int(lfps)-int(fps))
    if abs(int(lfps)-int(fps)) > 25:
        Ffps = fps

    cv2.putText(img, f'FPS:{int(Ffps)}', (400, 50),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
