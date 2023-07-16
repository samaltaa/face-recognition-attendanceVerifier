import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facedata-3a93d-default-rtdb.firebaseio.com/",
    'storageBucket':"facedata-3a93d.appspot.com"
})


# import images of the students
FolderPath = "Images"
PathList = os.listdir(FolderPath)
print(PathList)
imgList = []
studentIds =[]

for path in PathList:
    imgList.append(cv2.imread(os.path.join(FolderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    # this will send the images into the storage bucket in firebase
    fileName = f'{FolderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)



# function to create encodings
def findencodings(imagesList):
    encodelist = []
    for img in imagesList:

        # opencv uses BGR and Face_Recognition uses RGB, this swaps them
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # get encodings of first element of img
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)

    return encodelist

print("Encoding Started....")
encodeListKnown = findencodings(imgList)
encodingListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

file = open("EncodeFile.p", "wb")
pickle.dump(encodingListKnownWithIds, file)
file.close()
print("File Saved!")



