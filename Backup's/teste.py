from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from sqlite3 import *
import database as db


conn = None
conn = connect("cctv.db")
curs = conn.cursor()

if conn is not None:
    conn.close()    

conn = None
conn = connect("cctv.db")
curs = conn.cursor()
conn.commit()

if conn is not None:
    conn.close()

def show():
    ws_ent.delete(0, END)     
    ws_ent.focus()
    treeview.selection()
    conn = None
    try:
        conn = connect("cctv.db")    
        cursor = conn.cursor()
        db = "select * from cctv"   
        cursor.execute(db)

        fetchdata = treeview.get_children()       
        for elements in fetchdata:
            treeview.delete(elements)
    

        data = cursor.fetchall()
        for d in data:
            treeview.insert("", END, values=d)

        conn.commit()
    except Exception as e:
        showerror("Fail", e)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()

def search():
    treeview.selection()
    fetchdata = treeview.get_children()
    for f in fetchdata:
        treeview.delete(f)
    conn = None
    try:
        conn = connect("cctv.db")
        core = conn.cursor()
        db = "select * from cctv where nome = '%s' "
        name = ws_ent.get()
        if (len(name) < 2) or (not name.isalpha()):
            showerror("fail", "invalid nome")
        else:
            core.execute(db %(name))
            data = core.fetchall()
            for d in data:
                treeview.insert("", END, values=d)
            
    except Exception as e:
        showerror("issue", e)

    finally:
        if conn is not None:
            conn.close()

def reset():
    show()  

scrollbarx = Scrollbar(ws, orient=HORIZONTAL)  
scrollbary = Scrollbar(ws, orient=VERTICAL)    

treeview = ttk.Treeview(ws, columns=("id", "name", "apelido", "pontos"), show='headings', height=22)  
treeview.pack()
treeview.heading('id', text="ID", anchor=CENTER)
treeview.column("id", stretch=YES, width = 50) 
treeview.heading('name', text="Nome", anchor=CENTER)
treeview.column("name", stretch=NO)
treeview.heading('apelido', text="Apelido", anchor=CENTER)
treeview.column("apelido", stretch=NO)
treeview.heading('pontos', text="Pontos", anchor=CENTER)
treeview.column("pontos", stretch=NO)



scrollbary.config(command=treeview.yview)
scrollbary.place(x = 526, y = 7)
scrollbarx.config(command=treeview.xview)
scrollbarx.place(x = 220, y = 460)
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")


ws_lbl = Label(ws, text = "Nome", font=('calibri', 12, 'normal'))
ws_lbl.place(x = 290, y = 518)
ws_ent = Entry(ws,  width = 20, font=('Arial', 15, 'bold'))
ws_ent.place(x = 220, y = 540)
ws_btn1 = Button(ws, text = 'Procurar',  width = 8, font=('calibri', 12, 'normal'), command = search)
ws_btn1.place(x = 480, y = 540)
ws_btn2 = Button(ws, text = 'Reset',  width = 8, font=('calibri', 12, 'normal'), command = reset)
ws_btn2.place(x = 600, y = 540)

show()  

