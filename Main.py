import os
import trainer
import datasetCreator
import decade_image_storage
import var_config

def pro():
    '''This function is used to print wait message'''
    print("\nWait...")

def setcam():
    '''This function is used to set camera, which is used for face recognition, by default it is 0'''
    os.system("cls")
    print("set camera...")
    print()
    print("current camrera : "+str(var_config.which_cam))
    print()
    print()
    cam_no = input("Enter cam number: ")
    var_config.which_cam = int(cam_no)

# Main Menu, which shows the options to user to select from
while True:
    os.system('cls')
    print("Menu:")
    print("\t1) Create Database")
    print("\t2) Train Dataset")
    print("\t3) Recognize Face")
    print("\t4) Set Camera")
    print("\t5) Exit")
    print("\n")
    ch = input("Enter Option: ")
    if ch=='1':
        os.system('cls')
        #Creates the dataset
        #The dataset is created using the fun_datasetcreator() function
        datasetCreator.fun_datasetcreator()
    elif ch=='2':
        #Trains the dataset
        pro()
        trainer.fun_trainer()
    elif ch=='3':
        #Recognizes the face
        decade_image_storage.fun_decade_image_storage()
    elif ch=='4':
        #Set camera
        setcam()
    elif ch=='5':
        #Exit
        pro()
        exit()
    else:
        print("Please Enter vaild Choice...")