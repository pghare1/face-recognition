import cv2
import numpy as np
import sqlite3
import pickle
import urllib.request
import var_config
import time
import os

def getProfile(id):
    conn = sqlite3.connect("facebase.db")
    cmd = "SELECT * FROM people WHERE id=" + str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile

def fun_decade_image_storage():
    os.system("cls")
    print("\nWait...")
    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    if var_config.which_cam==0:
        cam=cv2.VideoCapture(1)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('recognizer/trainingData.yml')
    fontface = cv2.FONT_HERSHEY_SIMPLEX
    fontscale = 0.5
    fontcolor = (0, 255, 20)
    while(True):
        try:
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
                cv2.rectangle(img,(x,y),(x + w,y + h),(40,20,100),2)
                id,conf = recognizer.predict(gray[y:y + h,x:x + w])
                print(conf)
                if conf < 70:
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
