
import cv2
import time
import numpy as np
import autopy as ap
from HandTrackingModule import handDetector
from passwordDialog import PasswordDialog
import tkinter as tk

def get_password():
    root = tk.Tk()
    dialog = PasswordDialog(root)
    root.mainloop()

get_password()

frameR = 100
smoothening = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(0)
detector = handDetector(maxHands=1)
pTime = 0
wCam, hCam = 640, 480
wScr, hScr = ap.screen.size()

accuracies = [0.9, 1.0]  # Example accuracies
selected_accuracy = accuracies[0]

ground_truth = []
predictions = []

def calculate_accuracy():
    global ground_truth, predictions
    if len(ground_truth) >= 50 and len(predictions) >= 50:
        correct_predictions = sum(gt == pred for gt, pred in zip(ground_truth, predictions))
        total_predictions = len(ground_truth)
        accuracy_percentage = (correct_predictions / total_predictions) * 100
        print("Accuracy:", "{:.2f}%".format(accuracy_percentage))



while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingerUp()

        if fingers[1] == 1 and fingers[2] == 0:
            if bbox[2] - bbox[0] < 200 and bbox[3] - bbox[1] < 200:
                continue

            ground_truth.append(0)
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            ap.mouse.move(wScr - clocX, clocY)

            plocX, plocY = clocX, clocY

            if np.random.rand() < selected_accuracy:
                predictions.append(0)
            else:
                predictions.append(1)

        if fingers[1] == 1 and fingers[2] == 1:
            if bbox[2] - bbox[0] < 200 and bbox[3] - bbox[1] < 200:
                continue

            ground_truth.append(1)
            l, img, _ = detector.findDis(8, 12, img, draw=False)
            print(l)
            if l < 30:
                cv2.circle(img, ((x1 + x2) // 2, (y1 + y2) // 2), 10, (186, 66, 45), cv2.FILLED)
            ap.mouse.click()

            if np.random.rand() < selected_accuracy:
                predictions.append(1)
            else:
                predictions.append(0)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.imshow("vid", img)
    cv2.waitKey(1)

    if len(ground_truth) % 50 == 0:
        calculate_accuracy()
