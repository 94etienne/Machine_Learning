import cv2
cap = cv2.VideoCapture(0)
cap.set(3,1280) #width
cap.set(4,720) # height

while True:
    success, img = cap.read()    
    cv2.imshow("Face Attendance", img)
    cv2.waitKey(1) # 1 millisecond

# 
# PART  2: FIT WEBCAM TO SPECIFIED BACKGROUND
import cv2
cap = cv2.VideoCapture(0)
cap.set(3,480) #width
cap.set(4,360) # height

# Background
imgBackground = cv2.imread('Resources/background.png')
while True:
    success, img = cap.read() 
    
    #override camera to background H/W =(162:162+480, 55:55+640)
    # imgBackground[162:162+480, 55:55+640] = img
    # print(imgBackground.shape)
    img = cv2.resize(img, (480, 360))  # Resize img to 333x640
    # img = cv2.resize(img, (camera_width, camera_height))
    imgBackground[125:125+360, 26:26+480] = img  # Now this should work

  
    cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground) #Display Background
    cv2.waitKey(1) # 1 millisecond

    # PART 2 TAKE WEBCAM PHOTO AND FIT/OVERRIDE TO BACKGROUND
import cv2
cap = cv2.VideoCapture(0)
cap.set(3,480) #width
cap.set(4,360) # height

# Background
imgBackground = cv2.imread('Resources/background.png')
while True:
    success, img = cap.read() 
    
    #override camera to background H/W =(162:162+480, 55:55+640)
    # print(imgBackground.shape)
    img = cv2.resize(img, (480, 360))  # Resize img to 333x640
    imgBackground[104:104+360, 26:26+480] = img  # Now this should work

  
    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground) #Display Background
    cv2.waitKey(1) # 1 millisecond

# PART 3 CALL IMAGES RESULTS
import cv2
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


while True:
    success, img = cap.read() 
    
    #override camera to background H/W =(162:162+480, 55:55+640)
    # print(imgBackground.shape)
    img = cv2.resize(img, (480, 360))  # Resize img to 333x640
    imgBackground[104:104+360, 26:26+480] = img  # Now Background Image
    # Resize mode image to fit the target area (232x153)
    # Called Output Images from Image List Modes Folder
    mode_img_resized_imgModeList = cv2.resize(imgModeList[3], (153, 232))  # Width, Height
    imgBackground[104:104+232, 650:650+153] = mode_img_resized_imgModeList  # Overlay mode image
     

  
    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground) #Display Background
    cv2.waitKey(1) # 1 millisecond



# .........................Part 3.................................ENCODED GENERATOR IMAGES...............
import cv2
import face_recognition
import pickle
import os

# IMPORTING THE Students  IMAGES 
folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList= [] #load images in the list
studentsIds = [] #extract student img ids
print(pathList) #Print list of images
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path))) # append images to list
    # append images ids to student list
    studentsIds.append([os.path.splitext(path)[0]])
    # print(path) # print img with extension but not needed
    # # Split images ids with extension
    # print(os.path.splitext(path)[0]) # 0 means to get 1st element which is ID
    

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
file = open('EncodeFile.p','wb')
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("File Saved")


# ...........GENERATED PICKLE FILE FROM ABOVE CODES LOADED
import cv2
import pickle
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
    #override camera to background H/W =(162:162+480, 55:55+640)
    # print(imgBackground.shape)
    img = cv2.resize(img, (480, 360))  # Resize img to 333x640
    imgBackground[104:104+360, 26:26+480] = img  # Now Background Image
    # Resize mode image to fit the target area (232x153)
    # Called Output Images from Image List Modes Folder
    mode_img_resized_imgModeList = cv2.resize(imgModeList[2], (153, 232))  # Width, Height (Replace index 2 by variable to take detected image)
    imgBackground[104:104+232, 650:650+153] = mode_img_resized_imgModeList  # Overlay mode image   

    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground) #Display Background
    cv2.waitKey(1) # 1 millisecond



