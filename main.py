import os

import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# import the mode images into a list
FolderModePath = "Resources/Modes"
modePathList = os.listdir(FolderModePath)
imgModeList = []

for path in modePathList:
    # add image that has been imported
    imgModeList.append(cv2.imread(os.path.join(FolderModePath, path)))

# print(len(imgModeList))

while True:
    success, img = cap.read()

    img_resized = cv2.resize(imgModeList[1], (414, 633))

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[3]
    # cv2.imshow("Face Recognition", img)
    cv2.imshow("Registry", imgBackground)
    cv2.waitKey(1)
