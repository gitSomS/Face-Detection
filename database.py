import sqlite3

def connect():
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTs cctv (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT DEFAULT 'Desconhecido', apelido TEXT DEFAULT 'Desconhecido', idade INTEGER DEFAULT 'Desconhecido', pontos INTEGER DEFAULT '1000', crime TEXT DEFAULT 'Nenhum', id_match INTEGER, face BLOB)")
    conn.commit()
    conn.close()
    
def insert(nome,apelido,idade, id):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("UPDATE cctv SET nome=?, apelido=?, idade=? WHERE id=?",(nome, apelido, idade, id, ))
    conn.commit()
    conn.close()
    view()

def getNameFromID(id_match):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute('SELECT nome FROM cctv WHERE id_match = ?', (id_match, ))
    data = cur.fetchone()[0]
    conn.close()
    return data

def getPointsFromID(id_match):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute('SELECT pontos FROM cctv WHERE id_match = ?', (id_match, ))
    data = cur.fetchone()[0]
    conn.close()
    return data

def setPointsForID(pontos, id_match):
    print(pontos)
    print(id_match)
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("UPDATE cctv SET pontos=? where id_match=?",(pontos, id_match, ))
    conn.commit()
    conn.close()

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

def search(nome="",apelido="",pontos="",idade="",crime="",id_match=""):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM cctv WHERE nome=? OR apelido=? OR idade=? OR pontos=? OR crime=? OR id_match=?",(nome,apelido,idade,pontos,crime,id_match))
    row = cur.fetchall()
    conn.close()
    return row

def delete(id):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    #cur.execute("DELETE FROM cctv where id=?",(id,))
    cur.execute("UPDATE cctv SET nome= 'Desconhecido', apelido= 'Desconhecido', idade= 'Desconhecido' WHERE id=?",(id, ))
    conn.commit()
    conn.close()

def update(id,nome,apelido,idade):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("UPDATE cctv SET nome=? ,apelido=? , idade=? where id=?",(nome,apelido,idade,id))
    conn.commit()
    conn.close()

def read_file(filename):
    with open(filename, 'rb') as f:
        photo = f.read()
    return photo
    
def updateFace(face, id_match):
    conn = sqlite3.connect("cctv.db")
    cur = conn.cursor()
    cur.execute("UPDATE cctv SET face=? where id_match=?",(face, id_match, ))
    conn.commit()
    conn.close()

connect()