import cv2
import face_recognition
import pickle
import os

# import images of the students
FolderPath = "Images"
PathList = os.listdir(FolderPath)
print(PathList)
imgList = []
studentIds =[]

for path in PathList:
    # add image that has been imported
    imgList.append(cv2.imread(os.path.join(FolderPath, path)))
    # print(path)
    # print(os.path.splitext(path)[0])
    studentIds.append(os.path.splitext(path)[0])
print(studentIds)

# function to create encodings
def findencodings(imagesList):

    for img in imagesList:
        encodelist =[]
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



