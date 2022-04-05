import sqlite3

def connect():
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTs cctv (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT DEFAULT 'None', apelido TEXT, pontos INTEGER, crime TEXT, id_match INTEGER, face BLOB)")
    conn.commit()
    conn.close()
    
def insert(nome,apelido,pontos,crime):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO cctv VALUES (NULL, ?,?,?,?)",(nome,apelido,pontos,crime))
    conn.commit()
    conn.close()
    view()

def getNameFromID(id_match):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute('SELECT nome FROM cctv WHERE id_match = ?', (id_match, ))
    return str(cur.fetchone()[0])

def matchExist(id_match):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    response = cur.execute("SELECT EXISTS(SELECT id FROM cctv WHERE id_match=?)", (id_match, ))
    fetched = response.fetchone()[0]
    # if fetched == 1:
    #     print("sim")
    # else:
    #     print("nao")
    return fetched

def insertMatch(id_match):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO cctv(id_match) VALUES(?)",(id_match, ))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM cctv")
    row = cur.fetchall()
    conn.close()
    return row

def search(nome="",apelido="",pontos="",crime="",id_match=""):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM cctv WHERE nome=? OR apelido=? OR pontos=? OR crime=? OR id_match=?",(nome,apelido,pontos,crime,id_match))
    row = cur.fetchall()
    conn.close()
    return row

def delete(id):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM cctv where id=?",(id,))
    conn.commit()
    conn.close()

def update(id,nome,apelido,pontos,crime,id_match):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("UPDATE cctv SET nome=? ,apelido=? , pontos=? , crime=? , id_match=? where id=?",(nome,apelido,pontos,crime,id_match,id))
    conn.commit()
    conn.close()




connect()