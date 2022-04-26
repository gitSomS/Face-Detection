#====================================== IMPORTS =====================================#

from tkinter import *
import tkinter as tk, threading
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import Image,ImageTk
import database
import cv2
import os
import pickle
import time
import face_recognition
import database as db
import sqlite3
import time

#====================================== DEFINES =====================================#

KNOWN_FACES_DIR = "cctv_rostos" #pasta com os ID's 
TOLERANCE = 0.6 #valor maior = mais preciso
FRAME_THICKNESS = 3 #linha verde
FONT_THICKNESS = 2 #font
MODEL = "hog" #cnn

window=Tk()
window.attributes('-fullscreen', True)
window.title('CCTV Owner')
window.geometry("1920x1080")
window.iconbitmap(default="logo.ico")
main = Frame(window)
f1 = ("Arial", 20)
f2 = ("Arial", 10)

#====================================== FUNÇÕES =====================================#

def get_selected_row(event):
    global selected_tuple
    index = list1.focus()
    index2 = list1.item(index)["values"]
    
    selected_tuple = index2[0]
    
    nome_text.set(index2[1])
    apelido_text.set(index2[2])
    idade_text.set(index2[3])
    pontos_text.set(index2[4])
    obs_text.set(index2[5]) 
    id_match_text.set(index2[6]) 

def view_command():
    list1.delete(0,END)
    for row in database.view():
        list1.insert(END,row)

def search_command():
    list1.delete(0,END)
    for row in database.search(nome_text.get(),apelido_text.get(),idade_text.get(),pontos_text.get(),obs_text.get(),id_match_text.get()):
        list1.insert(END,row)

def edit_command():
    try:
        if selected_tuple and idade_text.get() > 0 and getState(selected_tuple) == 0 :
            database.insert(nome_text.get(),apelido_text.get(),idade_text.get(),obs_text.get(),selected_tuple)
            show()
            messagebox.showinfo("CCTV Owner", "Informação editada com sucesso!")
        else:
            messagebox.showwarning('CCTV Owner','Insira apenas números positivos na idade.')
        else:
            messagebox.showwarning('CCTV Owner','Insira apenas números positivos na idade.')    
    except NameError:
        messagebox.showwarning('CCTV Owner','Selecione o cidadão que deseja editar.')

def delete_command():
    try:
        if selected_tuple:
            res = messagebox.askquestion('CCTV Owner', 'Tem certeza que deseja remover o cidadão?')
            if res == 'yes':
                database.delete(selected_tuple)
                messagebox.showinfo('CCTV Owner', 'Cidadão removido com sucesso.')
                show()
            elif res == 'no':
                messagebox.showinfo('CCTV Owner', 'Tarefa cancelada.')
        else:
            messagebox.showwarning('CCTV Owner','Selecione o cidadão que deseja remover.')
    except NameError:
        messagebox.showerror('CCTV Owner','Contacte o fornecedor do sistema.')

def block_command():
    try:
        if selected_tuple:
            password = "teste"
            answer = simpledialog.askstring("CCTV Owner", "Insira a senha fornecida pelo sistema.")
            
            if answer == password:
                messagebox.showwarning('CCTV Owner','Cidadão Bloqueado com sucesso.')
                db.setState(1, selected_tuple)
            else:
                messagebox.showwarning('CCTV Owner','Senha Errada.')   
        else:
            messagebox.showwarning('CCTV Owner','Selecione o cidadão que deseja bloquear.')
    except NameError:
        messagebox.showwarning('CCTV Owner','Selecione o cidadão que deseja bloquear.')
    
def gosto():
    try:
        if selected_tuple:
            points = pontos_text.get()
            points = points + 1
            pontos_text.set(points)
            database.setPointsForID(points, selected_tuple)
            messagebox.showwarning("CCTV Owner", "O cidadao {0} recebeu +1 ponto.".format(nome_text.get()))
            show()
        else:
            messagebox.showwarning('CCTV Owner','Selecione o cidadão.')
    except NameError:
        messagebox.showwarning('CCTV Owner','Selecione o cidadão.')

def ngosto():
    try:
        if selected_tuple:
            points = pontos_text.get()
            points = points - 1
            pontos_text.set(points)
            database.setPointsForID(points, selected_tuple)
            messagebox.showwarning("CCTV Owner", "O cidadao {0} recebeu -1 ponto.".format(nome_text.get()))
    except NameError:
        messagebox.showwarning('CCTV Owner','Selecione o cidadão.')

def show():
    ws_ent.delete(0, END)     
    ws_ent.focus()
    list1.selection()
    conn = None
    try:
        conn = sqlite3.connect("cctv.db")    
        cursor = conn.cursor()
        db = "select * from cctv"   
        cursor.execute(db)

        fetchdata = list1.get_children()       
        for elements in fetchdata:
            list1.delete(elements)
    

        data = cursor.fetchall()
        for d in data:
            list1.insert("", END, values=d)

        conn.commit()
    except Exception as e:
        messagebox.showerror('Erro.', e)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()

def searchdata():
    list1.selection()
    fetchdata = list1.get_children()
    for f in fetchdata:
        list1.delete(f)
    conn = None
    try:
        conn = sqlite3.connect("cctv.db")
        core = conn.cursor()
        db = "select * from cctv where nome = '%s' "
        name = ws_ent.get()
        if (len(name) < 2) or (not name.isalpha()):
            messagebox.showerror('CCTV Owner','Erro.')

        else:
            core.execute(db %(name))
            data = core.fetchall()
            for d in data:
                list1.insert("", END, values=d)
            
    except Exception as e:
        showerror("issue", e)

    finally:
        if conn is not None:
            conn.close()

def reset():
    show()  

def naoFechar():
    messagebox.showwarning('CCTV Owner','Não estrague o projeto dos outros.')

# MOUSE EVENT VIDEO
#def mouseevent(event, x, y, flags, param):
    #if event == cv2.EVENT_LBUTTONDOWN:
    #print("Teste")
	
#====================================== DADOS - INFO - CIDADAO =====================================#
    
inf = LabelFrame(window,relief=SOLID)
inf.place(relx=0.7,rely=0.5, anchor="nw", relwidth=0.3,relheight=0.5)

nome_text=StringVar()
Label(inf, text="Nome").place(relx=0.35,rely=0.1, anchor="nw")
entry1 = Entry(window, textvariable=nome_text)
entry1.place(relx=0.85,rely=0.55, anchor="nw")

apelido_text=StringVar()
Label(inf, text="Apelido").place(relx=0.35,rely=0.2, anchor="nw")
entry2 = Entry(window, textvariable=apelido_text)
entry2.place(relx=0.85,rely=0.6, anchor="nw")

idade_text=IntVar() # CORRIGIR - INFO PARA INSERIR NUMEROS
Label(inf, text="Idade").place(relx=0.35,rely=0.3, anchor="nw")
entry3 = Entry(window, textvariable=idade_text)
entry3.place(relx=0.85,rely=0.65, anchor="nw")

obs_text=StringVar()
Label(inf, text="Observações").place(relx=0.35,rely=0.4, anchor="nw")
entry4 = Entry(window, textvariable=obs_text)
entry4.place(relx=0.85,rely=0.7, anchor="nw")

pontos_text=IntVar()
id_match_text=IntVar()

Button(inf, text="Adicionar Info", command=edit_command).place(relx=0.5,rely=0.55, anchor="center")
Button(inf, text="+1 Ponto", command=gosto).place(relx=0.3,rely=0.7, anchor="center")
Button(inf, text="-1 Ponto", command=ngosto).place(relx=0.7,rely=0.7, anchor="center")

#====================================== TITLE =====================================#

Label(main, text="CCTV Control", font=f1, relief=SOLID).place(relx=0.25, rely=0, anchor="nw", relwidth=0.45, relheight=0.1) 

#====================================== DATABASE - LISTBOX =====================================#

inf = LabelFrame(window,relief=SOLID)
inf.place(relx=0,rely=0.7, anchor="nw", relwidth=0.25,relheight=0.3)

scrollbarx = Scrollbar(window, orient=HORIZONTAL)  
scrollbary = Scrollbar(window, orient=VERTICAL)    

list1 = ttk.Treeview(window, columns=("id_match", "name", "apelido", "idade", "pontos"), show='headings', height=22)  
list1.place(relx=0, rely=0, anchor="nw", relwidth=0.25, relheight=0.7)
list1.heading('id_match', text="ID", anchor=CENTER)
list1.column("id_match", stretch=NO, width = 30) 
list1.heading('name', text="Nome", anchor=CENTER)
list1.column("name", stretch=NO, width = 112)
list1.heading('apelido', text="Apelido", anchor=CENTER)
list1.column("apelido", stretch=NO, width = 112)
list1.heading('idade', text="Idade", anchor=CENTER)
list1.column("idade", stretch=NO, width = 112)
list1.heading('pontos', text="Pontos", anchor=CENTER)
list1.column("pontos", stretch=NO, width = 112)

style = ttk.Style()
style.theme_use("default")
style.map("Treeview")
list1.bind('<ButtonRelease-1>', get_selected_row)

#Scrollbar - Desnecessário - Futuro
    #scrollbary.config(command=treeview.yview)
    #scrollbary.place(x = 480, y = 7)
    #scrollbarx.config(command=treeview.xview)
    #scrollbarx.place(x = 920, y = 960)

#====================================== CONFIG DATABASE =====================================#

Button(inf, text="Atualizar", command=reset).place(relx=0.6,rely=0.25, anchor="center")  
Button(inf, text="Bloquear Cidadão",command=block_command).place(relx=0.2,rely=0.25, anchor="center")

ws_lbl = Label(inf, text = "Nome", font=('calibri', 12, 'normal'))
ws_lbl.place(relx=0.1,rely=0.45)
ws_ent = Entry(inf,  width = 20, font=('Arial', 15, 'bold'))
ws_ent.place(relx=0.2,rely=0.45)
ws_btn1 = Button(inf, text = 'Procurar', command = searchdata)
ws_btn1.place(relx=0.8,rely=0.49, anchor="center")
ws_btn2 = Button(inf, text = 'Reset', command = reset)
ws_btn2.place(relx=0.8,rely=0.6, anchor="center")

show()

# CORRIGIR - BLOQUEAR MOVER TABELA - FUTURO
    #def handle_click(event):
    #    if treeview.identify_region(event.x, event.y) == "separator":
    #       return "break"
    #...
    #treeview.bind('<Button-1>', handle_click)

#====================================== DADOS - INFO - CIDADAO =====================================#

user = LabelFrame(window)
user.place(relx=0.7,rely=0, anchor="nw", relwidth=0.3,relheight=0.5)
Label(user, text="Info Cidadão", font=f1).place(relx=0.55, rely=0.05, anchor="center")

Label(user, text="Nome", textvariable = nome_text, font=f1).place(relx=0.55, rely=0.4, anchor="center")
Label(user, text="Apelido: ",textvariable=apelido_text, font=f1).place(relx=0.55, rely=0.5, anchor="center")
Label(user, text="Idade:",textvariable=idade_text, font=f1).place(relx=0.55, rely=0.6, anchor="center")
Label(user, text="Pontos:",textvariable=pontos_text, font=f1).place(relx=0.55, rely=0.7, anchor="center")
Label(user, text="Observações:",textvariable=obs_text, font=f1).place(relx=0.55, rely=0.8, anchor="center")
   
#====================================== CONFIG VIDEO =====================================#

Button(main,text="Em Construção",font=f1, relief=SOLID).place(relx=0.25, rely=0.7, anchor="nw", relwidth=0.45, relheight=0.3) 

#====================================== DEFINES VIDEO =====================================#

def main_f():
    main.pack(fill="both", expand=1)

    vid = LabelFrame(window,relief=SOLID)
    vid.place(relx=0.25,rely=0.1, anchor="nw", relwidth=0.45,relheight=0.6)
    window.update()
    width = vid.winfo_width()
    height = vid.winfo_height()

#================================ VIDEO / FACE DETECTION ============================#
 
    know_faces = []
    know_names = []

    global next_id
    
    for name in os.listdir(KNOWN_FACES_DIR):
        for filename in os.listdir(f"{KNOWN_FACES_DIR}\\{name}"):
            encoding = pickle.load(open (f"{KNOWN_FACES_DIR}/{name}/{filename}", "rb"))
            know_faces.append(encoding)
            know_names.append(int(name))

    if len(know_names) > 0:
        next_id = max(know_names) + 1
    else:
        next_id = 1

    video = cv2.VideoCapture(0)

    def display_video(label):
        while(video.isOpened()):
            frame, image = video.read()
           
            if frame == True:

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
                        next_id = len(know_faces) +1
                        match = str(next_id)
                        next_id += 1
                        
                        if db.matchExist(match) != 1:
                            db.insertMatch(match)
                        
                        know_names.append(match)
                        know_faces.append(face_encoding)
                        os.mkdir(f"{KNOWN_FACES_DIR}\\{match}")
                        pickle.dump(face_encoding, open(f"{KNOWN_FACES_DIR}\\{match}\\{match}-{int(time.time())}.pkl", "wb"))

#====================================== DESIGN VIDEO =====================================#

                    top_left = (face_location[3], face_location[0])
                    bottom_right = (face_location[1], face_location[2])
                    color = [0, 255, 0]
                
                    nomecidadao = db.getNameFromID(match)
                    pontoscidadao = db.getPointsFromID(match)
                    idadecidadao = db.getAgeFromID(match)
                    obscidadao = db.getObsFromID(match)

                    cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)
                
                    #CORRIGIR - ADJUST TO MOVIMENT
                    #res = cv2.addWeighted(sub_img, 0.5, white_rect, 0.5, 1.0)

                    cv2.rectangle(image, (face_location[3]+350, face_location[2]-200), (face_location[1]+10, face_location[2]-170), (82,82,82), cv2.FILLED)
                    cv2.rectangle(image, (face_location[3]+350, face_location[2]-160), (face_location[1]+10, face_location[2]-130), (82,82,82), cv2.FILLED)
                    cv2.rectangle(image, (face_location[3]+350, face_location[2]-120), (face_location[1]+10, face_location[2]-90), (82,82,82), cv2.FILLED)
                    cv2.rectangle(image, (face_location[3]+350, face_location[2]-80), (face_location[1]+10, face_location[2]-50), (82,82,82), cv2.FILLED)
                    cv2.rectangle(image, (face_location[3]+350, face_location[2]-40), (face_location[1]+10, face_location[2]-10), (82,82,82), cv2.FILLED)
                   
                    cv2.putText(image, "Cidadao: {}".format(match), (face_location[1]+20, face_location[2]-180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)
                    cv2.putText(image, "Nome: {}".format(nomecidadao), (face_location[1]+20, face_location[2]-140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)
                    cv2.putText(image, "Idade: {}".format(idadecidadao), (face_location[1]+20, face_location[2]-100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)                    
                    cv2.putText(image, "Pontos: {}".format(pontoscidadao), (face_location[1]+20, face_location[2]-60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)      
                    cv2.putText(image, "{}".format(obscidadao), (face_location[1]+20, face_location[2]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)      

#====================================== VIDEO =====================================#

                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(image)
                img2 = img.resize(((width,height)))
                image_frame = ImageTk.PhotoImage(image = img2)
                label.config(image=image_frame)
                label.image = image_frame         

    my_vid = Label(vid)
    my_vid.pack()
    thread = threading.Thread(target=display_video, args=(my_vid,))
    thread.start()

#====================================== CLOSE WINDOW =====================================#

window.protocol("WM_DELETE_WINDOW", naoFechar)
main_f()
window.mainloop()