import cv2
import numpy as np
import sqlite3
import pickle
import urllib.request
import var_config
import time
import os

def getProfile(id):
    '''This function is used to get the name of the user from the database, which is used for face recognition'''
    #SELECT query to get the information of the user from the database
    conn = sqlite3.connect("facebase.db")
    cmd = "SELECT * FROM people WHERE id=" + str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    #Returns the information of the user
    return profile

def fun_decade_image_storage():
    '''This function is used to create the dataset, which is used for face recognition, and save the data in the database'''
    os.system("cls")
    print("\nWait...")
    #Creates the faceDetect object
    #The faceDetect object is used to detect the face in the image
    #The faceDetect object is created using the haarcascade_frontalface_default.xml file
    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    if var_config.which_cam==0:
        cam=cv2.VideoCapture(1)
    #Creates the recognizer object
    #The recognizer object is used to recognize the face in the image
    #The recognizer object is created using the LBPHFaceRecognizer_create() function
    #The recognizer object is trained using the trainingData.yml file
    #The recognizer object is used to recognize the face in the image
    #The recognizer object is used to predict the face in the image
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('recognizer/trainingData.yml')
    fontface = cv2.FONT_HERSHEY_SIMPLEX
    fontscale = 0.5
    fontcolor = (0, 255, 20)
    while(True):
        try:
            #Reads the image from the camera
            #The image is read using the read() function
            #The image is stored in the img variable
            #The image is converted to gray scale
            #The image is converted to gray scale using the cvtColor() function
            #The image is stored in the gray variable
            if var_config.which_cam==0:
                ret,img=cam.read()
            elif var_config.which_cam==1:
                get_img = urllib.request.urlopen(var_config.ip)
                img = np.array(bytearray(get_img.read()),dtype=np.uint8)
                img = cv2.imdecode(img,-1)
            try:
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            except:
                if var_config.which_cam==0:
                    cam = cv2.VideoCapture(0)
                    ret,img = cam.read()
                    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
     
            try:
                #Detects the face in the image
                #The face is detected using the detectMultiScale() function
                #The face is stored in the faces variable
                faces = faceDetect.detectMultiScale(gray,1.3,5)
            except:
                print("no any camera found...")
                print("retry in 10 seconds...")
                try:
                    time.sleep(10)
                except KeyboardInterrupt:
                    break
                print()
                continue
            for(x,y,w,h) in faces:
                #Draws a rectangle around the face in the image
                #The rectangle is drawn using the rectangle() function
                cv2.rectangle(img,(x,y),(x + w,y + h),(40,20,100),2)
                id,conf = recognizer.predict(gray[y:y + h,x:x + w])
                print(conf)
                if conf < 70:
                    #Gets the name of the user from the database
                    #The name of the user is stored in the profile variable
                    #The information of the user is displayed on the image
                    profile = getProfile(id)
                    if(profile != None):
                         cv2.putText(img, "Name:-" + str(profile[1]), (x,y + h + 30), fontface, fontscale, fontcolor)
                         cv2.putText(img, "Country:-" + str(profile[3]), (x,y + h + 60), fontface, fontscale, fontcolor)
                         cv2.putText(img, "Crime Record:-" + str(profile[4]), (x,y + h + 90), fontface, fontscale, fontcolor)
                         cv2.putText(img, "State:-" + str(profile[5]), (x,y + h + 120), fontface, fontscale, fontcolor)
                         cv2.putText(img, "City:-" + str(profile[6]), (x,y + h + 150), fontface, fontscale, fontcolor)
                         cv2.imwrite("record/User." + str(id) + ".jpg",gray[y:y + h,x:x + w])
                else:
                    cv2.putText(img, "Uknown", (x,y + h + 30), fontface, fontscale, fontcolor)
                    cv2.imwrite("record/UnknownUser/User." + str(id) + ".jpg",gray[y:y + h,x:x + w])
                cv2.waitKey(25)
                cv2.imshow("SEQ CHECK",img)
        except KeyboardInterrupt:
            break
    if var_config.which_cam==0:
        cam.release()
    cv2.destroyAllWindows()
