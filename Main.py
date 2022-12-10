import os
import trainer
import datasetCreator
import decade_image_storage
import var_config

def pro():
    print("\nWait...")

def setcam():
    os.system("cls")
    print("set camera...")
    print()
    print("current camrera : "+str(var_config.which_cam))
    print()
    print()
    cam_no = input("Enter cam number: ")
    var_config.which_cam = int(cam_no)

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
        datasetCreator.fun_datasetcreator()
    elif ch=='2':
        pro()
        trainer.fun_trainer()
    elif ch=='3':
        decade_image_storage.fun_decade_image_storage()
    elif ch=='4':
        setcam()
    elif ch=='5':
        pro()
        exit()
    else:
        print("Please Enter vaild Choice...")