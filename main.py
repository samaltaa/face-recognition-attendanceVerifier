import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facedata-3a93d-default-rtdb.firebaseio.com/",
    'storageBucket':"facedata-3a93d.appspot.com"
})

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

# load encoding file
print("Loading Encoded File...")

file = open("EncodeFile.p", "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds

print("Encoded File Loaded!")

modeType = 0
counter = 0
id = -1

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

        matchIndex = np.argmin(faceDistance)
        # print("Match Index", matchIndex)

        if matches[matchIndex]:
            # print("Known Face Detected", matchIndex)
            print(studentIds[matchIndex])


        elif matches != True:
            # print("Unknown Face Detected", matchIndex)
            y1, x2, y2, x1 = faceLocation
            # we have to multiply it by 4 because in line 38 we reduced the size by 4
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            bbox = 55+x1, 162+y1, x2-x1, y2-y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt= 0)
            id = studentIds[matchIndex]

            # set counter to capture face encoding once in the first frame
            if counter == 0:
                counter = 1
    if counter != 0:
        if counter == 1:
            # download data of first frame
            studentInfo = db.reference(f'Employees/{id}').get()
            print(studentInfo)


        counter += 1

    cv2.imshow("Registry", imgBackground)
    cv2.waitKey(1)

