#====================================== IMPORTS =====================================#
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
import cv2 #opencv
import face_recognition #opencv
import os
import pickle
import time  #teste reduzir fps vídeo
import numpy as np
import sys
import database as db

#====================================== DEFINES =====================================#

KNOWN_FACES_DIR = "cctv_rostos" #pasta com os ID's 
TOLERANCE = 0.6 #valor maior = mais preciso
FRAME_THICKNESS = 3 #linha verde
FONT_THICKNESS = 2 #font
MODEL = "hog" #cnn
new_path ='D:/Faculdade/Projeto Artistico/Face Detection/rostos/_'
#C:\Users\SomS\Desktop\Rostos

window = Tk()

#window.minsize(height=1080,width=1920)
#window.geometry("1920x1080")
panel = Label(window)
panel.grid(row=0,column=2)

def naoFechar():
    messagebox.showwarning('CCTV Owner','Não estrague o projeto dos outros.')

def save(img, name, bbox, width=180, height=227):
    x,y,w,h = bbox
    imgCrop = img [y:h, x: w]
    imgCrop = cv2.resize(imgCrop, (width, height))
    cv2.imwrite(name+".jpg", imgCrop)

#====================================== VÍDEO =====================================#

video = cv2.VideoCapture(0) #nome do video ou link stream |  #Tela Cheia?
print("Carregando...") 

know_faces = []
know_names = []

for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f"{KNOWN_FACES_DIR}\\{name}"):
        encoding = pickle.load(open (f"{KNOWN_FACES_DIR}/{name}/{filename}", "rb"))
        know_faces.append(encoding)
        know_names.append(int(name))

if len(know_names) > 0:
    next_id = max(know_names) + 1
else:
    next_id = 0

#Loop for video stream
while True: 
    #video.set(cv2.CAP_PROP_FPS,10) PARA WEBCAM/LIVE
    #cv2.waitKey(100)
    stream = cv2.waitKey(1)   #Load video every 1ms and to detect user entered key

    frame, image = video.read()
    
    image = cv2.resize(image, (720, 480))

    locations = face_recognition.face_locations(image, model=MODEL)
    encodings = face_recognition.face_encodings(image, locations)
  
    for face_encoding, face_location in zip(encodings, locations):
        results = face_recognition.compare_faces(know_faces, face_encoding, TOLERANCE)
        match = None

        if True in results:
            match = know_names[results.index(True)]
            print(f"Pessoa ID: {match}")
            
            if db.matchExist(match) != 1:
                db.insertMatch(match)
            
                #save(image,new_path+str(encodings),(face_location[3], face_location[2],face_location[1], face_location[2]))


        else: # new id
            match = str(next_id)
            next_id += 1
            
            know_names.append(match)
            know_faces.append(face_encoding)
            os.mkdir(f"{KNOWN_FACES_DIR}\\{match}")
            pickle.dump(face_encoding, open(f"{KNOWN_FACES_DIR}\\{match}\\{match}-{int(time.time())}.pkl", "wb"))
            pickle.dump(face_encoding, open(f"{KNOWN_FACES_DIR}\\{match}\\{match}-{int(time.time())}.csv", "wb"))
            
            y1, x2, y2, x1 = face_location[0], face_location[1], face_location[2], face_location[3]
            save(image, new_path + match, (x1, y1, x2, y2))
            photo = db.read_file(new_path + match + ".jpg")

            #db.updateFace(photo, match)
            print(photo)
            #print(match)
            
            #save(image,new_path,(face_location[3], face_location[2],face_location[1], face_location[2]))
            #save(image,new_path+str(encodings),(x1-fit,y1-fit,x2+fit,y2+fit))


#====================================== DESIGN VÍDEO - GREEN SQUARE =====================================#

        top_left = (face_location[3], face_location[0])
        bottom_right = (face_location[1], face_location[2])
        color = [0, 255, 0]
        cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)
   
        cv2.rectangle(image, (face_location[3]+350, face_location[2]-200), (face_location[1]+10, face_location[2]-170), (82,82,82), cv2.FILLED)
        cv2.rectangle(image, (face_location[3]+350, face_location[2]-160), (face_location[1]+10, face_location[2]-130), (82,82,82), cv2.FILLED)
        cv2.rectangle(image, (face_location[3]+350, face_location[2]-110), (face_location[1]+10, face_location[2]-80), (82,82,82), cv2.FILLED)
        cv2.rectangle(image, (face_location[3]+350, face_location[2]-60), (face_location[1]+10, face_location[2]-30), (82,82,82), cv2.FILLED)

        nomecidadao = db.getNameFromID(match)
        pontoscidadao = db.getPointsFromID(match)

        cv2.putText(image, "Cidadao {}".format(match), (face_location[1]+20, face_location[2]-180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)
        cv2.putText(image, "Nome {}".format(nomecidadao), (face_location[1]+20, face_location[2]-140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)
        cv2.putText(image, "Pontos {}".format(pontoscidadao), (face_location[1]+20, face_location[2]-90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)      
        #cv2.putText(image, "Mais Info", (face_location[1]+20, face_location[2]-40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)
        
#====================================== OUTROS =====================================#

# Pressiona "q" para sair do vídeo
    cv2.namedWindow("CCTV Owner", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("CCTV Owner",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("CCTV Owner", image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break               

video.release()
#cv2.destroyAllWindows()
