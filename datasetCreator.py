import cv2
import numpy as np
import sqlite3
import os.path
import urllib.request
import var_config

def insertOrUpdate(id,name):
    conn = sqlite3.connect("facebase.db")
    cmd="SELECT * FROM people WHERE ID="+id
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE people SET name='"+name+"' WHERE id="+id
    else:
        cmd="INSERT INTO people(id,name) Values('"+ id +"','" + name +"')"
    conn.execute(cmd)
    conn.commit()
    conn.close()

def fun_datasetcreator():
    faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    while True:
        try:
            id=input('enter user id: ')
            name=input('enter your name: ')
            if(id==None or name==None):
                print("you enter null values")
                continue
            break
        except KeyboardInterrupt:
            print("\nctrl+c")
        except Exception as e:
            print("Exception Found: ",e)

    insertOrUpdate(id,name)
    sampleNumber=0
    if var_config.which_cam==0:
        cam=cv2.VideoCapture(1)

    while(True):
        try:
            if var_config.which_cam==0:
                ret,img=cam.read()
            elif var_config.which_cam==1:
                get_img = urllib.request.urlopen(var_config.ip)
                img = np.array(bytearray(get_img.read()),dtype=np.uint8)
                img = cv2.imdecode(img,-1)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        except:
            if var_config.which_cam==0:
                cam = cv2.VideoCapture(0)
                ret,img = cam.read()
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        faces=faceDetect.detectMultiScale(gray,1.3,5);
        for(x,y,w,h)in faces:
            sampleNumber=sampleNumber+1
            cv2.imwrite("dataSet/User."+str(id)+"."+str(sampleNumber)+".jpg",gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
            cv2.waitKey(100)
        cv2.imshow("Face",img)
        cv2.waitKey(25)
        if(sampleNumber>50):
            break
    cam.release()
    cv2.destroyAllWindows()
    print("\nSuccessfully Update or Insert...")
    input("\nPress Any Key to Exit...")