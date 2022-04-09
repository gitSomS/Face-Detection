from tkinter import *
import database
from tkinter import messagebox


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
    for row in database.search(nome_text.get(),apelido_text.get(),pontos_text.get(),crime_text.get(),id_match_text.get()):
        list1.insert(END,row)

def add_command():
    database.insert(nome_text.get(),apelido_text.get(),pontos_text.get(),crime_text.get())
    list1.delete(0,END)
    list1.insert(END,(nome_text.get(),apelido_text.get(),pontos_text.get(),crime_text.get()))
    messagebox.showinfo("CCTV Owner", "Informação adicionada com sucesso!")

def delete_command():
    database.delete(selected_tuple[0])

def update_command():
    database.update(selected_tuple[0],nome_text.get(),apelido_text.get(),pontos_text.get(),crime_text.get(),id_match_text.get())

def gosto():
    messagebox.showwarning("CCTV Owner", "O cidadao X recebeu +1 ponto.")

def ngosto():
    messagebox.showerror("CCTV Owner", "O cidadao X recebeu -1 ponto.")

window=Tk()
window.title('CCTV OWNER')
window.geometry("1920x1080")
video_path = "5.mp4" #paste your video path here

#====================================== VIDEO =====================================#



#====================================== TITLE =====================================#

label1=Label(window,text="CCTV EDIT")
label1.place(relx=0.25, rely=0, anchor="nw", relwidth=0.45, relheight=0.1) 

#====================================== DADOS - INFO - CIDADAO =====================================#
inf = LabelFrame(window,relief=SOLID)
inf.place(relx=0.7,rely=0.5, anchor="nw", relwidth=0.3,relheight=0.5)

label2=Label(inf,text="Nome")
label2.place(relx=0.35,rely=0.1, anchor="nw")

label3=Label(inf,text="Apelido")
label3.place(relx=0.35,rely=0.2, anchor="nw")

label4=Label(inf,text="Pontos")
label4.place(relx=0.35,rely=0.3, anchor="nw")

label5=Label(inf,text="Crime")
label5.place(relx=0.35,rely=0.4, anchor="nw")


nome_text=StringVar()
entry1=Entry(window,textvariable=nome_text)
entry1.place(relx=0.84,rely=0.55, anchor="nw")

apelido_text=StringVar()
entry2=Entry(window,textvariable=apelido_text)
entry2.place(relx=0.84,rely=0.6, anchor="nw")

pontos_text=StringVar()
entry3=Entry(window,textvariable=pontos_text)
entry3.place(relx=0.84,rely=0.65, anchor="nw")

crime_text=StringVar()
entry6=Entry(window,textvariable=crime_text)
entry6.place(relx=0.84,rely=0.7, anchor="nw")

b2=Button(inf,text="Adicionar Info",width=12,command=add_command)
b2.place(relx=0.5,rely=0.55, anchor="center")



#Button(inf, text="Adicionar Info", command=add_command).place(relx=0.5,rely=0.55, anchor="center")
Button(inf, text="+1 Ponto", command=gosto).place(relx=0.3,rely=0.7, anchor="center")
Button(inf, text="-1 Ponto", command=ngosto).place(relx=0.7,rely=0.7, anchor="center")


#====================================== DATABASE =====================================#
    #listbox
    #list1 = Listbox(root, relief=SOLID)
    #list1.place(relx=0, rely=0, anchor="nw", relwidth=0.25, relheight=0.7)
    #listbox.configure(state=DISABLED)

list1 = Listbox(window)
list1.place(relx=0, rely=0, anchor="nw", relwidth=0.25, relheight=0.7)
list1.bind('<<ListboxSelect>>',get_selected_row)

#scrl=Scrollbar(window)
#scrl.grid(row=1,column=0, padx = (10,0), sticky='ns',rowspan=2)

#list1.configure(yscrollcommand=scrl.set)
#scrl.configure(command=list1.yview)



#====================================== OPÇÕES DATABASE =====================================#
inf = LabelFrame(window, relief=SOLID)
inf.place(relx=0,rely=0.7, anchor="nw", relwidth=0.25,relheight=0.3)

b1=Button(inf,text="Ver todos",width=12, command=view_command)
b1.place(relx=0.6,rely=0.25, anchor="center")  

b3=Button(inf,text="Apagar Info",width=12,command=delete_command)
b3.place(relx=0.2,rely=0.25, anchor="center")

b4=Button(inf,text="Procurar",width=12,command=search_command)
b4.place(relx=0.2,rely=0.55, anchor="center")

b5=Button(inf,text="Atualizar",width=12,command=update_command)
b5.place(relx=0.6,rely=0.55, anchor="center")             


window.mainloop()


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




    #listbox
    #list1 = Listbox(root, relief=SOLID)
    #list1.place(relx=0, rely=0, anchor="nw", relwidth=0.25, relheight=0.7)
    #listbox.configure(state=DISABLED)

list1 = Listbox(window)
list1.place(relx=0, rely=0, anchor="nw", relwidth=0.25, relheight=0.7)
view_command()

#scrl=Scrollbar(window)
#scrl.grid(row=1,column=0, padx = (10,0), sticky='ns',rowspan=2)

#list1.configure(yscrollcommand=scrl.set)
#scrl.configure(command=list1.yview)


list1.bind('<<ListboxSelect>>',get_selected_row)