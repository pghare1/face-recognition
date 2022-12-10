import os
import cv2
import numpy as np
from PIL import Image

def getImagesWithID(path):
    '''This function is used to get images and their corresponding IDs, which are used for training, from the dataset folder'''
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
        faceImg=Image.open(imagePath).convert('L');
        faceNp=np.array(faceImg,'uint8')
        ID=int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(ID)
        cv2.imshow("training",faceNp)
        cv2.waitKey(10)
    return np.array(IDs), faces

def fun_trainer():
    '''This function is used to train the dataset, which is used for face recognition, and save the trained data in a file'''
    recognizer=cv2.face.LBPHFaceRecognizer_create();
    path='dataset'
    Ids,faces=getImagesWithID(path)
    recognizer.train(faces,np.array(Ids))
    recognizer.write('recognizer//trainingData.yml')
    cv2.destroyAllWindows()


