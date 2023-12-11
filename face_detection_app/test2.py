import cv2
import pickle
import face_recognition
import numpy as np
import cvzone
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
bucket = storage.bucket()
# end upload to db

cap = cv2.VideoCapture(0)
cap.set(3,480) #width
cap.set(4,360) # height
# Background
imgBackground = cv2.imread('Resources/background.png')
# IMPORTING THE MODES IMAGES INTO A LIST
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList= [] #load images in the list
# print(modePathList) #Print list of images
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path))) # append images to list
# print(len(imgModeList)) #print total imgs




# LOAD THE ENCODING FILE
print('Loading Encode File...')
file = open('EncodeFile.p','rb') #reading permission
encodeListKnownWithIds = pickle.load(file)
file.close()
# Separate into 2 parts
encodeListKnown,studentsIds = encodeListKnownWithIds
# print(studentsIds)
print('Encode File Loaded')

#for db downloading image only once
modeType = 0 
counter = 0
id = -1 # id of image (0 is also item of image)
imgStudent= []

# end db

while True:
    success, img = cap.read()   

    # SQUEZE IMAGES TO SMALLER image FOR OPTIMIZATION
    imgS = cv2.resize(img,(0,0),None,0.25,0.25) 
    imgS= cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB) 
    # end smaller
    # Face Recognition for faces in our folder or picle file
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)   # end

   
    #override camera to background H/W =(162:162+480, 55:55+640)
    # print(imgBackground.shape)
    img = cv2.resize(img, (480, 360))  # Resize img to 333x640
    imgBackground[104:104+360, 26:26+480] = img  # Now Background Image
    # Resize mode image to fit the target area (232x153)
    # Called Output Images from Image List Modes Folder
    # Width, Height (Replace index 2 by variable to take detected image)
    # mode_img_resized_imgModeList = cv2.resize(imgModeList[0], (153, 232))      
    mode_img_resized_imgModeList = cv2.resize(imgModeList[modeType], (153, 232)) 
    imgBackground[104:104+232, 650:650+153] = mode_img_resized_imgModeList  # Overlay mode image 

    # extracting/matches faces
    for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDist = face_recognition.face_distance(encodeListKnown,encodeFace) #Lower distance better match
        # print("Matches", matches)
        # print("FaceDistance", faceDist)

        matchIndex = np.argmin(faceDist)
        # print("Match Index", matchIndex)

        if matches[matchIndex]:
            # print("Known Face Detected")
            # print(studentsIds[matchIndex])
            # Draw Rectangle around the face
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4  # its divided into 4 (imgS = cv2.resize(img,(0,0),None,0.25,0.25))
            bbox = 0 + x1, 90 + y1, x2-x1, y2-y1 #(Adjust numbers to make rectangle fit in your eyes)
            imgBackground=cvzone.cornerRect(imgBackground,bbox,rt=0) #rt (rectangle technas)

            # download image db
            # it was previous 0 then be 1
            id = studentsIds[matchIndex]
            # print(id)
            if counter == 0:
                counter =1
                modeType=1 # update mode (Info)
        if counter!= 0:
            # 1st frame
            if counter == 1:
                # Students table created on db firebase
                # Get Data
                studentInfo= db.reference(f'Students/{id}').get() # download Image
                print(studentInfo)
                # Get Image From Storage of firebase
                blob = bucket.get_blob(f'Images/{id}.PNG')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                # imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)
                
                # UPDATING DATA OF ATTENDANCE
                ref = db.reference(f'Students/{id}')
                studentInfo['total_attendance'] +=1 #increment attendance in db
                ref.child('total_attendance').set(studentInfo['total_attendance']) # antendance updated in db
            # Set time to capture antendance
            if 10<counter<20:
                modeType = 2
                mode_img_resized_imgModeList = cv2.resize(imgModeList[modeType], (153, 232)) 
                imgBackground[104:104+232, 650:650+153] = mode_img_resized_imgModeList  # Overlay mode image 

            if counter<=10:
                # 861,125 location where output displayed 1 is size white color (255,255,255) thinkness 1
                # cv2.putText(imgBackground,str(studentInfo['total_attendance']),(861,125),
                # cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                cv2.putText(imgBackground,str(studentInfo['total_attendance']),(663,140),
                cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
                cv2.putText(imgBackground,str(studentInfo['name']),(590,80),
                cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),1)
                cv2.putText(imgBackground,str(studentInfo['major']),(590,390),
                cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),1)
                cv2.putText(imgBackground,str(id),(590,365),
                cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),1)
                cv2.putText(imgBackground,str(studentInfo['standing']),(590,420),
                cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),1)
                cv2.putText(imgBackground,str(studentInfo['year']),(590,340),
                cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),1)
                cv2.putText(imgBackground,str(studentInfo['starting_year']),(590,320),
                cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),1)
                cv2.putText(imgBackground,str(studentInfo['qualification']),(590,440),
                cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),1)
                
                # Add name in Center
                # (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                # offset = (414-w)//2
                # cv2.putText(imgBackground, str(studentInfo['name']), (590+offset, 80), 
                #             cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)


                #(Copy Image take to specified area)(Download once but co)
                # Resize imgStudent to fit into the 216x216 square.

                # img = cv2.resize(img, (480, 360))  # Resize img to 333x640
                # imgBackground[104:104+360, 26:26+480] = img  # Now Background Image
                
                imgStudent_resized = cv2.resize(imgStudent, (90, 90))
                imgBackground[150:150+90, 685:685+90] = imgStudent_resized

                # right_offset = 100
                # imgBackground[104:104+200, (26+right_offset):(26+right_offset)+200] = imgStudent_resized

                # print(imgBackground.shape)           
            
            counter+=1
            # Reseting everything
            if counter >= 20:
                counter = 0
                modeType = 0
                studentInfo = []
                imgStudent = []
                mode_img_resized_imgModeList = cv2.resize(imgModeList[modeType], (153, 232)) 
                imgBackground[104:104+232, 650:650+153] = mode_img_resized_imgModeList  # Overlay mode image 

            

        # else:
        #     print("Unknown Face In Database")


    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground) #Display Background
    cv2.waitKey(1) # 1 millisecond

