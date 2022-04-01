#====================================== IMPORTS =====================================#
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import face_recognition
import numpy as np
#====================================== DEFINES =====================================#
UPSAMPLE = 1 #valor maior = mais preciso
RESOLUTION = "1366x768"
USE_RECONGNITION = 0

print("Carregando TkInter...")
root = Tk()
root.geometry(RESOLUTION)
root.configure(bg="#1E90FF")
testes = Label(root, text="CCTV", font=("times new roman", 30, "bold"), bg="#1E90FF").pack()
f1 = LabelFrame(root, bg="#FFA500")
f1.pack()
l1 = Label(f1, bg="#FFA500")
l1.pack()

def mouse_events(event,x,y,flags,param):  
    print("{}".format(event))
    if event == cv2.EVENT_LBUTTONDBLCLK:
        button1=Button(root, text="button1")
        button1.place(x, y)

print("Carregando OpenCV...")
cascadePath = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
video = cv2.VideoCapture("casemito.mp4") 
cv2.namedWindow('image')  
cv2.setMouseCallback('image',mouse_events)  

#Vars
locations = []
while True: 
    frame, image = video.read()

    #face_recognition
    if USE_RECONGNITION == 0:
        small_frame = cv2.resize(image, (0, 0), fx=0.50, fy=0.50)

        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb_frame, UPSAMPLE)

    #Cascade
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    cascade_faces = cascadePath.detectMultiScale(gray,
                                         scaleFactor=1.3,
                                         minNeighbors=7,
                                         minSize=(60, 60),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
    if len(locations) <= 0 and USE_RECONGNITION == 0:
        print('Usando cascade')
        for (x,y,w,h) in cascade_faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255,255,0), 2)
            cv2.putText(image, "{}".format(cascade_faces), (x, y + 25), cv2.FONT_HERSHEY_SIMPLEX,0.75, (255,215,0), 2)
            cv2.putText(image, "cascade {}".format(len(cascade_faces)), (x, h), cv2.FONT_HERSHEY_SIMPLEX,0.75, (255,215,0), 2)
    else:
        print('Usando face_locations')
        for (top, right, bottom, left) in locations:
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2
            cv2.rectangle(image, (left, top), (right, bottom), (30,144,255), 2)
            cv2.putText(image, "{}".format(locations), (left, bottom + 25), cv2.FONT_HERSHEY_SIMPLEX,0.75, (65,105,225), 2)
            cv2.putText(image, "face_locations {}".format(len(locations)), (left, top), cv2.FONT_HERSHEY_SIMPLEX,0.75, (65,105,225), 2)

    if len(cascade_faces) <= 0 and len(locations) <= 0:
        print('cabo')
        #TODO: Implementar detector/hog
    
    img1 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img2 = ImageTk.PhotoImage(Image.fromarray(img1))
    l1['image'] = img2
    root.update()

video.release()
