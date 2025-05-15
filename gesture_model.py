import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

# gesture_model.py
class GestureRecognizer:
    def __init__(self, model_path, labels_path, labels_list=None):
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(maxHands=2)
        #self.detector = HandDetector(maxHands=2)
        #self.detector.hands.static_image_mode = True  # Manually set MediaPipe's internal mode


        self.classifier = Classifier(model_path, labels_path)
        self.offset = 20
        self.imgSize = 300
        self.labels = labels_list or ["goodbye", "hello","help","nice","yes"]
        self.current_prediction = "Detecting..."  # Default label

    def get_prediction(self):
        return self.current_prediction

    def start(self):
        import threading
        thread = threading.Thread(target=self._run_camera, daemon=True)
        thread.start()

    def _run_camera(self):
        while True:
            success, img = self.cap.read()
            imgOutput = img.copy()
            hands, img = self.detector.findHands(img)

            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']
                imgWhite = np.ones((self.imgSize, self.imgSize, 3), np.uint8) * 255
                try:
                    imgCrop = img[y - self.offset:y + h + self.offset, x - self.offset:x + w + self.offset]
                    aspectRatio = h / w

                    if aspectRatio > 1:
                        k = self.imgSize / h
                        wCal = math.ceil(k * w)
                        imgResize = cv2.resize(imgCrop, (wCal, self.imgSize))
                        wGap = math.ceil((self.imgSize - wCal) / 2)
                        imgWhite[:, wGap: wCal + wGap] = imgResize
                    else:
                        k = self.imgSize / w
                        hCal = math.ceil(k * h)
                        imgResize = cv2.resize(imgCrop, (self.imgSize, hCal))
                        hGap = math.ceil((self.imgSize - hCal) / 2)
                        imgWhite[hGap: hCal + hGap, :] = imgResize

                    prediction, index = self.classifier.getPrediction(imgWhite, draw=False)
                    self.current_prediction = self.labels[index]

                except Exception as e:
                    self.current_prediction = "Error"
                    print("Prediction error:", e)

    def predict_frame(self, img):
        imgOutput = img.copy()
        hands, img = self.detector.findHands(img)
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            try:
                imgWhite = np.ones((self.imgSize, self.imgSize, 3), np.uint8) * 255
                imgCrop = img[y - self.offset:y + h + self.offset, x - self.offset:x + w + self.offset]
                aspectRatio = h / w

                if aspectRatio > 1:
                    k = self.imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, self.imgSize))
                    wGap = math.ceil((self.imgSize - wCal) / 2)
                    imgWhite[:, wGap: wCal + wGap] = imgResize
                else:
                    k = self.imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (self.imgSize, hCal))
                    hGap = math.ceil((self.imgSize - hCal) / 2)
                    imgWhite[hGap: hCal + hGap, :] = imgResize

                prediction, index = self.classifier.getPrediction(imgWhite, draw=False)
                return self.labels[index]

            except Exception as e:
                print("Prediction error:", e)
                return "Error"
        return "No hand"

'''
    def predict_frame(self, img):
        hands, _ = self.detector.findHands(img)
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            try:
                imgWhite = np.ones((self.imgSize, self.imgSize, 3), np.uint8) * 255
                imgCrop = img[y - self.offset:y + h + self.offset, x - self.offset:x + w + self.offset]
                aspectRatio = h / w

                if aspectRatio > 1:
                    k = self.imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, self.imgSize))
                    wGap = math.ceil((self.imgSize - wCal) / 2)
                    imgWhite[:, wGap: wCal + wGap] = imgResize
                else:
                    k = self.imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (self.imgSize, hCal))
                    hGap = math.ceil((self.imgSize - hCal) / 2)
                    imgWhite[hGap: hCal + hGap, :] = imgResize

                prediction, index = self.classifier.getPrediction(imgWhite, draw=False)
                #prediction, index = self.classifier.getPrediction(imgWhite, draw=False)
                if prediction[index] > 0.80:
                     self.current_prediction = self.labels[index]
                else:
                    self.current_prediction = "Uncertain"

                return self.labels[index]
            except Exception as e:
                print("Prediction error:", e)
        return "No hand"

'''