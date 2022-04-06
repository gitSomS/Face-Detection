from tkinter import *
import tkinter as tk, threading
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo
import imageio
from PIL import Image,ImageTk
import database
import cv2


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

def add_command():
    database.insert(nome_text.get(),apelido_text.get(),pontos_text.get(),crime_text.get())
    list1.delete(0,END)
    list1.insert(END,(nome_text.get(),apelido_text.get(),pontos_text.get(),crime_text.get()))
    messagebox.showinfo("CCTV Owner", "Informação adicionada com sucesso!")

def delete_command():
    if selected_tuple[0] != None:
        res = messagebox.askquestion('CCTV Owner', 'Tem certeza que deseja remover o cidadão?')
        if res == 'yes':
            database.delete(selected_tuple[0])
            messagebox.showinfo('CCTV Owner', 'Cidadão removido com sucesso.')
            view_command()
        elif res == 'no':
            messagebox.showinfo('CCTV Owner', 'Tarefa cancelada.')
    else:
        messagebox.showwarning('CCTV Owner','Selecione o cidadão que deseja remover.')
    
def gosto():
    #PEGAR OS PONTOS_TEXT E INSERIR +1 PONTO
    messagebox.showwarning("CCTV Owner", "O cidadao X recebeu +1 ponto.")

def ngosto():
    #Escolher um cidadao primeiro
    #SENAO MANDAR MENSAGEM PARA ESCOLHER CIDADAO
    #PEGAR OS PONTOS_TEXT E INSERIR -1 PONTO
    messagebox.showerror("CCTV Owner", "O cidadao X recebeu -1 ponto.")

window=Tk()
window.title('CCTV OWNER')
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


Button(inf, text="Adicionar Info", command=add_command).place(relx=0.5,rely=0.55, anchor="center")
Button(inf, text="+1 Ponto", command=gosto).place(relx=0.3,rely=0.7, anchor="center")
Button(inf, text="-1 Ponto", command=ngosto).place(relx=0.7,rely=0.7, anchor="center")

#====================================== TITLE =====================================#
Label(main, text="CCTV Control", font=f1, relief=SOLID).place(relx=0.25, rely=0, anchor="nw", relwidth=0.45, relheight=0.1) 

#====================================== DATABASE - LISTBOX =====================================#

    #listbox
    #list1 = Listbox(root, relief=SOLID)
    #list1.place(relx=0, rely=0, anchor="nw", relwidth=0.25, relheight=0.7)
    #listbox.configure(state=DISABLED)

list1 = Listbox(window)
list1.place(relx=0, rely=0, anchor="nw", relwidth=0.25, relheight=0.7)

#scrl=Scrollbar(window)
#scrl.grid(row=1,column=0, padx = (10,0), sticky='ns',rowspan=2)

#list1.configure(yscrollcommand=scrl.set)
#scrl.configure(command=list1.yview)


list1.bind('<<ListboxSelect>>',get_selected_row)

#====================================== CONFIG DATABASE =====================================#

inf = LabelFrame(window,relief=SOLID)
inf.place(relx=0,rely=0.7, anchor="nw", relwidth=0.25,relheight=0.3)

Button(inf, text="Ver Todos", command=view_command).place(relx=0.6,rely=0.25, anchor="center")  
Button(inf, text="Atualizar", command=view_command).place(relx=0.6,rely=0.55, anchor="center")
Button(inf, text="Procurar").place(relx=0.2,rely=0.55, anchor="center")
Button(inf, text="Apagar Info",command=delete_command).place(relx=0.2,rely=0.25, anchor="center")

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
    video = imageio.get_reader(video_path)
    
    def display_video(label):
    # iterate through video data
        for image in video.iter_data():
            # convert array into image
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