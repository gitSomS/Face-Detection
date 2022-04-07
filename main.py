from tkinter import *
import tkinter as tk, threading
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo
import imageio
from PIL import Image,ImageTk
import database
import cv2
import os
import pickle
import face_recognition #opencv
import database as db




KNOWN_FACES_DIR = "cctv_rostos" #pasta com os ID's 
TOLERANCE = 0.6 #valor maior = mais preciso
FRAME_THICKNESS = 3 #linha verde
FONT_THICKNESS = 2 #font
MODEL = "hog" #cnn

#====================================== DEFINES =====================================#

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
    entry5.insert(END,selected_tuple[4])


def update_command():
    database.update(selected_tuple[0],nome_text.get(),apelido_text.get(),pontos_text.get(),crime_text.get(),id_match_text.get())

def view_command():
    list1.delete(0,END)
    for row in database.view():
        list1.insert(END,row)

def search_command():
    list1.delete(0,END)
    for row in database.search(nome_text.get(),apelido_text.get(),pontos_text.get(),crime_text.get(),id_match_text.get()):
        list1.insert(END,row)

def searchtable():
    treeview.selection()
    fetchdata = treeview.get_children()
    for f in fetchdata:
        treeview.delete(f)
    conn = None
    try:
        conn = connect("cctv.db")
        core = conn.cursor()
        db = "select * from cctv where nome = '%s' "
        nome = ws_ent.get()
        if (len(nome) < 2) or (not nome.isalpha()):
            showerror("fail", "invalid nome")
        else:
            core.execute(db %(nome))
            data = core.fetchall()
            for d in data:
                treeview.insert("", END, values=d)
            
    except Exception as e:
        showerror("issue", e)

    finally:
        if conn is not None:
            conn.close()

def add_command():
    database.insert(nome_text.get(),apelido_text.get(),pontos_text.get(),crime_text.get())
    list1.delete(0,END)
    list1.insert(END,(nome_text.get(),apelido_text.get(),pontos_text.get(),crime_text.get()))
    view_command()
    messagebox.showinfo("CCTV Owner", "Informação adicionada com sucesso!")

def delete_command():
    try:
        if selected_tuple[0]:
            res = messagebox.askquestion('CCTV Owner', 'Tem certeza que deseja remover o cidadão?')
            if res == 'yes':
                database.delete(selected_tuple[0])
                messagebox.showinfo('CCTV Owner', 'Cidadão removido com sucesso.')
                view_command()
            elif res == 'no':
                messagebox.showinfo('CCTV Owner', 'Tarefa cancelada.')
        else:
            messagebox.showwarning('CCTV Owner','Selecione o cidadão que deseja remover.')
    except NameError:
        messagebox.showwarning('CCTV Owner','Selecione o cidadão que deseja remover.')
    
def gosto():
    try:
        if selected_tuple[5]:
            points = database.getPointsFromID(selected_tuple[5])

            points + 1

            database.setPointsForID(points, selected_tuple[5])
            messagebox.showwarning("CCTV Owner", "O cidadao {5} recebeu +1 ponto.".points)
    except NameError:
        messagebox.showwarning('CCTV Owner','Selecione o cidadão.')

def ngosto():
    #Escolher um cidadao primeiro
    #SENAO MANDAR MENSAGEM PARA ESCOLHER CIDADAO
    #PEGAR OS PONTOS_TEXT E INSERIR -1 PONTO
    messagebox.showerror("CCTV Owner", "O cidadao X recebeu -1 ponto.")

def mouseevent(event, x, y, flags, param):
	
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Teste")
	

window=Tk()
window.title('CCTV Owner')
window.geometry("1920x1080")
#window.iconbitmap('D:\\images\\favicon.ico')
main = Frame(window)
f1 = ("Arial", 20)
f2 = ("Arial", 10)
video_path = "5.mp4" #paste your video path here

#====================================== DADOS - INFO - CIDADAO =====================================#
    
inf = LabelFrame(window,relief=SOLID)
inf.place(relx=0.7,rely=0.5, anchor="nw", relwidth=0.3,relheight=0.5)

nome_text=StringVar()
Label(inf, text="Nome").place(relx=0.35,rely=0.1, anchor="nw")
entry1 = Entry(window, textvariable=nome_text)
entry1.place(relx=0.84,rely=0.55, anchor="nw")

apelido_text=StringVar()
Label(inf, text="Apelido").place(relx=0.35,rely=0.2, anchor="nw")
entry2 = Entry(window, textvariable=apelido_text)
entry2.place(relx=0.84,rely=0.6, anchor="nw")

pontos_text=StringVar()
Label(inf, text="Pontos").place(relx=0.35,rely=0.3, anchor="nw")
entry3 = Entry(window, textvariable=pontos_text)
entry3.place(relx=0.84,rely=0.65, anchor="nw")

crime_text=StringVar()
Label(inf, text="Crime").place(relx=0.35,rely=0.4, anchor="nw")
entry4 = Entry(window, textvariable=crime_text)
entry4.place(relx=0.84,rely=0.7, anchor="nw")

id_match_text=StringVar()
entry5 = Entry(window, textvariable=id_match_text)



Button(inf, text="Adicionar Info", command=add_command).place(relx=0.5,rely=0.55, anchor="center")
Button(inf, text="+1 Ponto", command=gosto).place(relx=0.3,rely=0.7, anchor="center")
Button(inf, text="-1 Ponto", command=ngosto).place(relx=0.7,rely=0.7, anchor="center")

#====================================== TITLE =====================================#
Label(main, text="CCTV Control", font=f1, relief=SOLID).place(relx=0.25, rely=0, anchor="nw", relwidth=0.45, relheight=0.1) 

#====================================== DATABASE - LISTBOX =====================================#

inf = LabelFrame(window,relief=SOLID)
inf.place(relx=0,rely=0.7, anchor="nw", relwidth=0.25,relheight=0.3)

scrollbarx = Scrollbar(inf, orient=HORIZONTAL)  
scrollbary = Scrollbar(inf, orient=VERTICAL)    

treeview = ttk.Treeview(inf, columns=("rollno", "name"), show='headings', height=22)  
treeview.pack()
treeview.heading('rollno', text="Roll No", anchor=CENTER)
treeview.column("rollno", stretch=NO, width = 100) 
treeview.heading('name', text="Name", anchor=CENTER)
treeview.column("name", stretch=NO)


#scrollbary.config(command=treeview.yview)
#scrollbary.place(x = 526, y = 7)
#scrollbarx.config(command=treeview.xview)
#scrollbarx.place(x = 220, y = 460)
#style = ttk.Style()
#style.theme_use("default")
#style.map("Treeview")


#ws_lbl = Label(inf, text = "Name", font=('calibri', 12, 'normal').place(relx=0, rely=0, anchor="nw", relwidth=0.25, relheight=0.7))
#ws_ent = Entry(inf,  width = 20, font=('Arial', 15, 'bold').place(relx=0, rely=0)
#ws_btn1 = Button(inf, text = 'Search',  width = 8, font=('calibri', 12, 'normal'), command = search)
#ws_btn1.place(x = 480, y = 540)
#ws_btn2 = Button(inf, text = 'Reset',  width = 8, font=('calibri', 12, 'normal'), command = reset)
#ws_btn2.place(x = 600, y = 540)

#====================================== CONFIG DATABASE =====================================#

inf = LabelFrame(window,relief=SOLID)
inf.place(relx=0,rely=0.7, anchor="nw", relwidth=0.25,relheight=0.3)

Button(inf, text="Atualizar", command=view_command).place(relx=0.6,rely=0.25, anchor="center")  
Button(inf, text="Apagar Info",command=delete_command).place(relx=0.2,rely=0.25, anchor="center")

ws_lbl = Label(inf, text = "Nome", font=('calibri', 12, 'normal')).place(relx=0.1,rely=0.45)
ws_ent = Entry(inf,  width = 20, font=('Arial', 15, 'bold')).place(relx=0.2,rely=0.45)
ws_btn1 = Button(inf, text = 'Procurar').place(relx=0.8,rely=0.49, anchor="center")
ws_btn2 = Button(inf, text = 'Resetar').place(relx=0.8,rely=0.6, anchor="center")



#====================================== DADOS - INFO - CIDADAO =====================================#

user = LabelFrame(window)
user.place(relx=0.7,rely=0, anchor="nw", relwidth=0.3,relheight=0.5)

Label(user, text="Info Cidadão", font=f1).place(relx=0.4, rely=0.05, anchor="nw")
Label(user, text="Foto",textvariable=nome_text, font=f1).place(relx=0.5, rely=0.3, anchor="nw")
Label(user, text="Nome:",textvariable=nome_text, font=f1).place(relx=0.5, rely=0.5, anchor="nw")
Label(user, text="Apelido:",textvariable=apelido_text, font=f1).place(relx=0.5, rely=0.6, anchor="nw")
Label(user, text="Pontos:",textvariable=pontos_text, font=f1).place(relx=0.5, rely=0.7, anchor="nw")
Label(user, text="Crime:",textvariable=crime_text, font=f1).place(relx=0.5, rely=0.8, anchor="nw")
   
#====================================== CONFIG VIDEO =====================================#

Button(main,text="Em Construção",font=f1, relief=SOLID).place(relx=0.25, rely=0.7, anchor="nw", relwidth=0.45, relheight=0.3) 

#====================================== VIDEO =====================================#

def main_f():
    main.pack(fill="both", expand=1)

    vid = LabelFrame(window,relief=SOLID)
    vid.place(relx=0.25,rely=0.1, anchor="nw", relwidth=0.45,relheight=0.6)
    window.update()
    width = vid.winfo_width()
    height = vid.winfo_height()


#FACE DETECTION
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

    video = cv2.VideoCapture(0)

    def display_video(label):
    # iterate through video data
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
                        match = str(next_id)
                        next_id += 1
                        
                        know_names.append(match)
                        know_faces.append(face_encoding)
                        os.mkdir(f"{KNOWN_FACES_DIR}\\{match}")
                        pickle.dump(face_encoding, open(f"{KNOWN_FACES_DIR}\\{match}\\{match}-{int(time.time())}.pkl", "wb"))
                        pickle.dump(face_encoding, open(f"{KNOWN_FACES_DIR}\\{match}\\{match}-{int(time.time())}.csv", "wb"))
                                
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

                #for image in video.iter_data():
                    # convert array into image
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(image)
                img2 = img.resize(((width,height)))
                    # Convert image to PhotoImage
                image_frame = ImageTk.PhotoImage(image = img2)
                
                # configure video to the lable
                label.config(image=image_frame)
                label.image = image_frame
    # create and start thread
    my_vid = Label(vid)
    my_vid.pack()
    thread = threading.Thread(target=display_video, args=(my_vid,))
    thread.start()
              
main_f()
window.mainloop()