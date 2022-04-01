import sqlite3

def connect():
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTs cctv (id INTEGER PRIMARY KEY , nome TEXT , apelido TEXT , pontos INTEGER , crime TEXT, face BLOB)")
    conn.commit()
    conn.close()
    
def insert(nome,apelido,pontos,crime):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO cctv VALUES (NULL, ?,?,?,?)",(nome,apelido,pontos,crime))
    conn.commit()
    conn.close()
    view()

def view():
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM cctv")
    row = cur.fetchall()
    conn.close()
    return row

def search(nome="",apelido="",pontos="",crime=""):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM cctv WHERE nome=? OR apelido=? OR pontos=?  OR crime=?",(nome,apelido,pontos,crime))
    row = cur.fetchall()
    conn.close()
    return row

def delete(id):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM cctv  where id=?",(id,))
    conn.commit()
    conn.close()

def update(id,nome,apelido,pontos,crime):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("UPDATE cctv SET nome=? ,apelido=? , pontos=? , crime=? where id=?",(nome,apelido,pontos,crime,id))
    conn.commit()
    conn.close()

connect()