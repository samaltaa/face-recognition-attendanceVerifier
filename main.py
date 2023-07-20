import os
import pickle
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facedata-3a93d-default-rtdb.firebaseio.com/",
    'storageBucket':"facedata-3a93d.appspot.com"
})

bucket = storage.bucket()
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
imgStudent =[]

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # capture frame and location of the face in camera
    faceCurrentFrame = face_recognition.face_locations(imgS)
    encodeCurrentFrame = face_recognition.face_encodings(imgS, faceCurrentFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurrentFrame:
        # use the zip method to iterate both arrays
        # extract encoding and location of the face in frame
        for encodeFace, faceLocation in zip(encodeCurrentFrame, faceCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDistance)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:

                y1, x2, y2, x1 = faceLocation
                # we have to multiply it by 4 because in line 38 we reduced the size by 4
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55+x1, 162+y1, x2-x1, y2-y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt= 0)
                id = studentIds[matchIndex]

                # set counter to capture face encoding once in the first frame
                if counter == 0:
                    # add "loading" message on screen while data loads
                    cvzone.putTextRect(imgBackground, "Loading...", (275, 400))
                    cv2.imshow("Registry", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1
        if counter != 0:
            # download data
            if counter == 1:

                studentInfo = db.reference(f'Employees/{id}').get()
                print(studentInfo)
                # get image from storage in database
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # update attendance data
                datetimeObject = datetime.strptime(studentInfo['Last Attendance Time'],
                                                  "%y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                print(secondsElapsed)
                # TODO: change the number of seconds to the number that corresponds with how many seconds in employee shift

                if secondsElapsed > 30:

                    ref = db.reference(f'Employees/{id}')
                    studentInfo['Total Attendance'] += 1
                    ref.child('Total Attendance').set(studentInfo['Total Attendance'])
                    # update time and date of last clock in
                    ref.child('Last Attendance Time').set(datetime.now().strftime("%y-%m-%d %H:%M:%S"))
                else:
                    modeType = 0
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 0:

                if 10<counter<20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:

                    # add the student/employee info to the GUI
                    cv2.putText(imgBackground, str(studentInfo['Total Attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1,(255, 255, 255), 1)

                    cv2.putText(imgBackground, str(studentInfo['Position']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                    cv2.putText(imgBackground, str(studentInfo['Standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    cv2.putText(imgBackground, str(studentInfo['Year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    cv2.putText(imgBackground, str(studentInfo['Starting Year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w,h), _ = cv2.getTextSize(studentInfo['Name'], cv2.FONT_HERSHEY_COMPLEX, 1,1)
                    offset = (414-w)//2
                    cv2.putText(imgBackground, str(studentInfo['Name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175+216, 909:909+216] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 3
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 3
        counter = 0
    cv2.imshow("Registry", imgBackground)
    cv2.waitKey(1)

