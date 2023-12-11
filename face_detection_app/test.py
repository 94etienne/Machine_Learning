import cv2
import pickle
import face_recognition
import numpy as np
import cvzone
import os
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
    mode_img_resized_imgModeList = cv2.resize(imgModeList[3], (153, 232))  # Width, Height (Replace index 2 by variable to take detected image)
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
            

        else:
            print("Unknown Face In Database")


    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground) #Display Background
    cv2.waitKey(1) # 1 millisecond

