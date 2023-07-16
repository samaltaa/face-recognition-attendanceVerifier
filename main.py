import os
import pickle
import cv2
import face_recognition
import numpy as np

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

# load encoding file
print("Loading Encoded File...")

file = open("EncodeFile.p", "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encoded File Loaded!")

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # capture frame and location of the face in camera
    faceCurrentFrame = face_recognition.face_locations(imgS)
    encodeCurrentFrame = face_recognition.face_encodings(imgS, faceCurrentFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[3]

    # use the zip method to iterate both arrays
    # extract encoding and location of the face in frame
    for encodeFace, faceLocation in zip(encodeCurrentFrame, faceCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print("matches", matches)
        # print("faceDistance", faceDistance)

        matchIndex = np.argmin(faceDistance)
        print("Match Index", matchIndex)

        if matches[matchIndex]:
            print("Known Face Detected")
        elif matches != True:
            print("unknown face")

    # cv2.imshow("Face Recognition", img)
    cv2.imshow("Registry", imgBackground)
    cv2.waitKey(1)
