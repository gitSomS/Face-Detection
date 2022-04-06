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

window = Tk()
window.minsize(height=720,width=720)
panel = Label(window)
panel.grid(row=0,column=2)

def get_selected_row(event):
    global selected_tuple
    index=list1.curselection()[0]
    selected_tuple=list1.get(index)
    entry1.delete(0,END)
    entry1.insert(END,selected_tuple[1])
    entry2.delete(0,END)
    entry2.insert(END,selected_tuple[2])
    entry3.delete(0,END)
    entry3.insert(END,selected_tuple[3])
    entry4.delete(0,END)
    entry4.insert(END,selected_tuple[4])
    entry5.delete(0,END)
    entry5.insert(END,selected_tuple[5])
    entry6.delete(0,END)
    entry6.insert(END,selected_tuple[6])

def view_command():
    list1.delete(0,END)
    for row in database.view():
        list1.insert(END,row)

def search_command():
    list1.delete(0,END)
    for row in database.search(nome_text.get(),apelido_text.get(),pontos_text.get(),crime_text.get()):
        list1.insert(END,row)

def add_command():
    database.insert(nome_text.get(),apelido_text.get(),pontos_text.get(),crime_text.get())
    list1.delete(0,END)
    list1.insert(END,(nome_text.get(),apelido_text.get(),pontos_text.get(),crime_text.get()))

def delete_command():
    database.delete(selected_tuple[0])

def update_command():
    database.update(selected_tuple[0],nome_text.get(),apelido_text.get(),pontos_text.get(),crime_text.get())

#====================================== WINDOW - MANIPULATION - TKINTER =====================================#

def tab1():

    def ngosto():
        messagebox.showerror("Aviso", "O cidadao X recebeu -1 ponto.")

    def gosto():
        messagebox.showerror("Aviso", "O cidadao X recebeu +1 ponto.")

    def remover():
        label1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        label2 = Label(window, text="Deseja remover todos os dados da pessoa X?",font=("Times_New_Roman",25))
        label2.grid()
        #FAZER PERGUNTA - Se sim, notificação a dizer que foi removida e volta ao vídeo
        #               - Se não, volta ao tab1. 

    def cctvcontrol():
        label1.destroy()
        button1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        button5.destroy()

        label6=Label(window,text="CCTV EDIT")
        label6.grid(row=0,column=2, padx = (100,0), pady = (10,50))

        label2=Label(window,text="Nome")
        label2.grid(row=1,column=0)

        label3=Label(window,text="Apelido")
        label3.grid(row=2,column=0)

        label4=Label(window,text="Pontos")
        label4.grid(row=3,column=0)

        label5=Label(window,text="Crime")
        label5.grid(row=4,column=0)

        nome_text=StringVar()
        entry1=Entry(window,textvariable=nome_text)
        entry1.grid(row=1,column=1)

        apelido_text=StringVar()
        entry2=Entry(window,textvariable=apelido_text)
        entry2.grid(row=2,column=1)

        pontos_text=StringVar()
        entry3=Entry(window,textvariable=pontos_text)
        entry3.grid(row=3,column=1)

        crime_text=StringVar()
        entry6=Entry(window,textvariable=crime_text)
        entry6.grid(row=4,column=1)

        list1=Listbox(window,height=20,width=59)
        list1.grid(row=1,column=3, rowspan=6, columnspan=2, padx = (0,50))

        scrl=Scrollbar(window)
        scrl.grid(row=1,column=2, sticky='ns',rowspan=6)

        list1.configure(yscrollcommand=scrl.set)
        scrl.configure(command=list1.yview)


        list1.bind('<<ListboxSelect>>',get_selected_row)

        b1=Button(window,text="Ver todos",width=12, command=view_command)
        b1.grid(row=7, column=0)

        b2=Button(window,text="Adicionar Info",width=12,command=add_command)
        b2.grid(row=8, column=0)

        b3=Button(window,text="Apagar Info",width=12,command=delete_command)
        b3.grid(row=10, column=0)

        b4=Button(window,text="Procurar",width=12,command=search_command)
        b4.grid(row=7, column=1)

        b5=Button(window,text="Atualizar",width=12,command=update_command)
        b5.grid(row=8, column=1)

           
    label1 = Label(window, text="CCTV Admin",font=("Times_New_Roman",25))
    label1.grid(row=1,column=1, ipadx = 400, pady = (50,250))

    button1 = Button(window, text="Gosto",font=("Times_New_Roman",15),command=gosto, activebackground="blue")
    button1.grid(row=2,column=1, pady = 10)

    button2 = Button(window, text="Não Gosto",font=("Times_New_Roman",15),command=ngosto, activebackground="blue")
    button2.grid(row=3,column=1, pady = 10)

    button3 = Button(window, text="Editar Info",font=("Times_New_Roman",15),command=cctvcontrol, activebackground="blue")
    button3.grid(row=4,column=1, pady = 10)

    button4 = Button(window, text="Remover Cidadao",font=("Times_New_Roman",15),command=remover, activebackground="blue")
    button4.grid(row=5,column=1, pady = 10)

    #FAZER - Se botão "Voltar" tiver no tab1, volta ao vídeo, se não, volta ao tab1
    button5 = Button(window, text="Voltar",font=("Times_New_Roman",15), activebackground="blue")
    button5.grid(row=6,column=1, pady = 10)

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

def mouseevent(event, x, y, flags, param):
	
    if event == cv2.EVENT_LBUTTONDOWN:
        video.release()
        tab1()
        window.mainloop()
	
	
cv2.namedWindow("image")
cv2.setMouseCallback("image", mouseevent)

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

            if db.matchExist(match) != 1:
                db.insertMatch(match)

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
     
        cv2.rectangle(image, (face_location[3]+350, face_location[2]-200), (face_location[1]+10, face_location[2]-170), (82,82,82), cv2.FILLED)
        cv2.rectangle(image, (face_location[3]+350, face_location[2]-160), (face_location[1]+10, face_location[2]-130), (82,82,82), cv2.FILLED)
        cv2.rectangle(image, (face_location[3]+350, face_location[2]-110), (face_location[1]+10, face_location[2]-80), (82,82,82), cv2.FILLED)
        cv2.rectangle(image, (face_location[3]+350, face_location[2]-60), (face_location[1]+10, face_location[2]-30), (82,82,82), cv2.FILLED)

        nomecidadao = db.getNameFromID(match)
        pontoscidadao = db.getPointsFromID(match)

        cv2.putText(image, "Cidadao {}".format(match), (face_location[1]+20, face_location[2]-180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)
        cv2.putText(image, "Nome {}".format(nomecidadao), (face_location[1]+20, face_location[2]-140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)
        cv2.putText(image, "Pontos {}".format(pontoscidadao), (face_location[1]+20, face_location[2]-90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)      
        cv2.putText(image, "Mais Info", (face_location[1]+20, face_location[2]-40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)



#====================================== OUTROS =====================================#


# Pressiona "q" para sair do vídeo
    cv2.imshow("image", image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break               

video.release()
#cv2.destroyAllWindows()


window.mainloop()