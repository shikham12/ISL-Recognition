import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

# !pip install cvzone

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2)
offset = 20
imgSize = 300
counter = 0

folder = r"C:\Users\study\Downloads\yes"

# +
while True:
    success, img = cap.read()
    if not success:
        break

    # Detect hands in the frame
    hands, img = detector.findHands(img)

    if hands and len(hands) > 0:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        # Print for debugging
        print(f"Bounding Box: x={x}, y={y}, w={w}, h={h}")

        # Create a white canvas image to place the resized cropped hand image
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

        # Crop the hand region from the frame ensuring indices do not go out of bounds
        y1 = max(0, y - offset)
        y2 = min(img.shape[0], y + h + offset)
        x1 = max(0, x - offset)
        x2 = min(img.shape[1], x + w + offset)
        imgCrop = img[y1:y2, x1:x2]
        
        # Check if the crop has valid dimensions
        if imgCrop.shape[0] > 0 and imgCrop.shape[1] > 0:
            aspectRatio = h / w
            # Resize and place into imgWhite maintaining aspect ratio
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize

            cv2.imshow('ImageCrop', imgCrop)
            cv2.imshow('ImageWhite', imgWhite)
        else:
            print("Invalid crop dimensions")

    cv2.imshow('Image', img)
    
    # Wait for key press for 1 ms
    key = cv2.waitKey(1) & 0xFF
    
    # If 's' is pressed, save the white image
    if key == ord("s"):
        counter += 1
        imgName = f'{folder}/Image_{time.time()}.jpg'
        cv2.imwrite(imgName, imgWhite)
        print(f"Saved image #{counter} as {imgName}")
    
    # Add an exit condition (press 'q' to quit)
    if key == ord("q"):
        print("Exiting...")
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()

# -









