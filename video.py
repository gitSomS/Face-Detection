#====================================== IMPORTS =====================================#
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import cv2 #opencv
import face_recognition #opencv
import os
import pickle
import time  #teste reduzir fps vídeo
import numpy as np
import sys
import database

#====================================== DEFINES =====================================#

KNOWN_FACES_DIR = "cctv_rostos" #pasta com os ID's 
TOLERANCE = 0.4 #valor maior = mais preciso
FRAME_THICKNESS = 3 #linha verde
FONT_THICKNESS = 2 #font
MODEL = "hog" #cnn

window = Tk()
window.minsize(height=720,width=720)
panel = Label(window)
panel.pack(padx=5, pady=5)

#====================================== WINDOW - MANIPULATION - TKINTER =====================================#
#Ao clicar no quadrado verde, cria a janela de "Manipulação"

def tab1():

    def ngosto():
        label1.destroy()
        button1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        label2 = Label(window, text="- 1 Ponto no ID x",font=("Times_New_Roman",25))
        label2.pack()
        def back():
            label2.destroy()
            button5.destroy()
            tab1()
        button5 = Button(window, text='Voltar', font=("Times_New_Roman", 25), command=back, activebackground="blue")
        button5.pack(side=BOTTOM)
        #FAZER - temporizador | após 5s na tela, volta ao tab1

    def gosto():
        label1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        button5.destroy()
        
        label2 = Label(window, text="+ 1 Ponto no ID x",font=("Times_New_Roman",25))
        label2.pack()
        def back():
            label2.destroy()
            button5.destroy()
            tab1()
        button5 = button(window, text="Voltar", font=("Times_New_Roman", 25), command=back, activebackground="blue")
        button5.pack(side=BOTTOM)
        #FAZER - temporizador | após 5s na tela, volta ao tab1

    def remover():
        label1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        label2 = Label(window, text="Deseja remover todos os dados da pessoa X?",font=("Times_New_Roman",25))
        label2.pack()
        #FAZER PERGUNTA - Se sim, notificação a dizer que foi removida e volta ao vídeo
        #               - Se não, volta ao tab1. 
    
    label1 = Label(window, text="CCTV Admin",font=("Times_New_Roman",25))
    label1.pack()

    #FAZER - Se botão "Voltar" tiver no tab1, volta ao vídeo, se não, volta ao tab1
    button1 = Button(window, text="Voltar",font=("Times_New_Roman",15), activebackground="blue")
    button1.pack(side=BOTTOM, pady=10)

    button2 = Button(window, text="Remover Cidadao",font=("Times_New_Roman",15),command=remover, activebackground="blue")
    button2.pack(side=BOTTOM, pady=10)

    button3 = Button(window, text="Editar Info",font=("Times_New_Roman",15),command=remover, activebackground="blue")
    button3.pack(side=BOTTOM, pady=10)
    #editinfo.py

    button4 = Button(window, text="Não Gosto",font=("Times_New_Roman",15),command=ngosto, activebackground="blue")
    button4.pack(side=BOTTOM, pady=10)
    button5 = Button(window, text="Gosto",font=("Times_New_Roman",15),command=gosto, activebackground="blue")
    button5.pack(side=BOTTOM, pady=10)

#====================================== VÍDEO =====================================#

#image = cv2.imread('abba.png') #Imagem em vez de Video
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
  
    locations = face_recognition.face_locations(image, model=MODEL)
    encodings = face_recognition.face_encodings(image, locations)
    
    for face_encoding, face_location in zip(encodings, locations):
        results = face_recognition.compare_faces(know_faces, face_encoding, TOLERANCE)
        match = None
        if True in results:
            match = know_names[results.index(True)]
            print(f"Pessoa ID: {match}")
        else: # new id
            match = str(next_id)
            next_id += 1
            
            know_names.append(match)
            know_faces.append(face_encoding)
            os.mkdir(f"{KNOWN_FACES_DIR}\\{match}")
            pickle.dump(face_encoding, open(f"{KNOWN_FACES_DIR}\\{match}\\{match}-{int(time.time())}.pkl", "wb"))
            pickle.dump(face_encoding, open(f"{KNOWN_FACES_DIR}\\{match}\\{match}-{int(time.time())}.csv", "wb"))


#====================================== DESIGN VÍDEO - GREEN SQUARE =====================================#

        top_left = (face_location[3], face_location[0])
        bottom_right = (face_location[1], face_location[2])
        color = [0, 255, 0]
        cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)
        
        top_left = (face_location[3], face_location[2])
        bottom_right = (face_location[1], face_location[2]+22)
        cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
        #Error
        #cv2.putText(image, match, (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), FONT_THICKNESS)

#====================================== OUTROS =====================================#

# Pressiona "q" para sair do vídeo
    cv2.imshow("", image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break               

video.release()
#cv2.destroyAllWindows()

tab1()
window.mainloop()