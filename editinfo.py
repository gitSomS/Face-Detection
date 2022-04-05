from tkinter import *
import database

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

def delete_command():
    database.delete(selected_tuple[0])

def update_command():
    database.update(selected_tuple[0],nome_text.get(),apelido_text.get(),pontos_text.get(),crime_text.get(),id_match_text.get())

window=Tk()
window.title('CCTV OWNER')
window.minsize(height=1080,width=1920)

label1=Label(window,text="CCTV EDIT")
label1.grid(row=0,column=3)

label2=Label(window,text="Nome")
label2.grid(row=1,column=4, padx = (900,0), pady = (50,0))

label3=Label(window,text="Apelido")
label3.grid(row=2,column=4, padx = (900,0), pady = (50,1))

label4=Label(window,text="Pontos")
label4.grid(row=3,column=4, padx = (900,0), pady = (50,1))

label5=Label(window,text="Crime")
label5.grid(row=4,column=4, padx = (900,0), pady = (50,1))

b2=Button(window,text="Adicionar Info",width=12,command=add_command)
b2.grid(row=5, column=4, padx = (900,0), pady = (50,1))


nome_text=StringVar()
entry1=Entry(window,textvariable=nome_text)
entry1.grid(row=1,column=5, padx = (20,0), pady = (0,0))

apelido_text=StringVar()
entry2=Entry(window,textvariable=apelido_text)
entry2.grid(row=2,column=5)

pontos_text=StringVar()
entry3=Entry(window,textvariable=pontos_text)
entry3.grid(row=3,column=5)

crime_text=StringVar()
entry6=Entry(window,textvariable=crime_text)
entry6.grid(row=4,column=5)

list1=Listbox(window,height=35,width=59)
list1.grid(row=0,column=0, padx = (100,0), pady = (0,0), rowspan=6, columnspan=1)

scrl=Scrollbar(window)
scrl.grid(row=1,column=0, padx = (10,0), sticky='ns',rowspan=2)

list1.configure(yscrollcommand=scrl.set)
scrl.configure(command=list1.yview)


list1.bind('<<ListboxSelect>>',get_selected_row)

b1=Button(window,text="Ver todos",width=12, command=view_command)
b1.grid(row=7, column=0)

b3=Button(window,text="Apagar Info",width=12,command=delete_command)
b3.grid(row=10, column=0)

b4=Button(window,text="Procurar",width=12,command=search_command)
b4.grid(row=7, column=1)

b5=Button(window,text="Atualizar",width=12,command=update_command)
b5.grid(row=8, column=1)             


window.mainloop()