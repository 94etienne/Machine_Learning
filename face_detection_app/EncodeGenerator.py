import cv2
import face_recognition
import pickle
import os

# Upload Images to a Database
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
cred = credentials.Certificate("serviceAccountKey.json") #credentials
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://faceantendancerealtime-default-rtdb.firebaseio.com/', #From Real time database link
    'storageBucket': 'faceantendancerealtime.appspot.com' #from storage link (except https://)

})
# end upload to db

# IMPORTING THE Students  IMAGES 
folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList= [] #load images in the list
studentsIds = [] #extract student img ids
print(pathList) #Print list of images
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path))) # append images to list
    # append images ids to student list
    # studentsIds.append([os.path.splitext(path)[0]])
    studentsIds.append(os.path.splitext(path)[0])
    # print(path) # print img with extension but not needed
    # # Split images ids with extension
    # print(os.path.splitext(path)[0]) # 0 means to get 1st element which is ID
    # .............Upload Image To a DB...........................

    fileName= f'{folderPath}/{path}' #this will create folder called images and include all local images on firebase storage
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    

    

# print(len(imgList)) #print total imgs
print(studentsIds)

# CREATE A LIST FOR ENCODINGS
def findEncodings(imagesList):
    encodeList = []
    # Look through images and encodes each imgs
    for img in imagesList:
        # Convert Color
        cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0] #1st imgs
        encodeList.append(encode) # look for imgs and save it
    return encodeList

# All known Faces
print("Encoding Started...")
encodeListKnown = findEncodings(imgList) #call imgList define above
# Save imgs in a Pickle file
encodeListKnownWithIds =[encodeListKnown,studentsIds]
# print(encodeListKnown)
print("Encoding Complete")
file = open('EncodeFile.p','wb') # writting permission
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("File Saved")
