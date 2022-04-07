from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from sqlite3 import *


ws = Tk()                       
ws.title("Python Guides")        
ws.geometry("750x700+400+50")  
ws.resizable(0, 0)            
      



conn = None

conn = connect("data1.db")

  
curs = conn.cursor()


db = "create table student(rno int primary key, name text)"
curs.execute(db)


if conn is not None:
    conn.close()    



conn = None


conn = connect("data1.db")


curs = conn.cursor()


db1 = "insert into student values(1,'Pauline')"
db2 = "insert into student values(2,'Dexter')"
db3 = "insert into student values(3,'Melba')"
db4 = "insert into student values(4,'Roxanne')"
db5 = "insert into student values(5,'Mary')"
db6 = "insert into student values(6,'Andrew')"
db7 = "insert into student values(7,'Renata')"


curs.execute(db1)
curs.execute(db2)
curs.execute(db3)
curs.execute(db4)
curs.execute(db5)
curs.execute(db6)
curs.execute(db7)


conn.commit()


if conn is not None:
    conn.close()


def show():
    ws_ent.delete(0, END)     
    ws_ent.focus()
    treeview.selection()
    conn = None
    try:
        conn = connect("data1.db")    
        cursor = conn.cursor()
        db = "select * from student"   
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
        conn = connect("data1.db")
        core = conn.cursor()
        db = "select * from student where name = '%s' "
        name = ws_ent.get()
        if (len(name) < 2) or (not name.isalpha()):
            showerror("fail", "invalid name")
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

treeview = ttk.Treeview(ws, columns=("rollno", "name"), show='headings', height=22)  
treeview.pack()
treeview.heading('rollno', text="Roll No", anchor=CENTER)
treeview.column("rollno", stretch=NO, width = 100) 
treeview.heading('name', text="Name", anchor=CENTER)
treeview.column("name", stretch=NO)


scrollbary.config(command=treeview.yview)
scrollbary.place(x = 526, y = 7)
scrollbarx.config(command=treeview.xview)
scrollbarx.place(x = 220, y = 460)
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")


ws_lbl = Label(ws, text = "Name", font=('calibri', 12, 'normal'))
ws_lbl.place(x = 290, y = 518)
ws_ent = Entry(ws,  width = 20, font=('Arial', 15, 'bold'))
ws_ent.place(x = 220, y = 540)
ws_btn1 = Button(ws, text = 'Search',  width = 8, font=('calibri', 12, 'normal'), command = search)
ws_btn1.place(x = 480, y = 540)
ws_btn2 = Button(ws, text = 'Reset',  width = 8, font=('calibri', 12, 'normal'), command = reset)
ws_btn2.place(x = 600, y = 540)


show()  
ws.mainloop()
