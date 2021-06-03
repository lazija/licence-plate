import sqlite3
import os

conn = sqlite3.connect('zaposleni.db')
cur = conn.cursor()

def connect():

    conn = sqlite3.connect("zaposleni.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS data1 (id Integer PRIMARY KEY, ime TEXT, prezime TEXT, tablice TEXT, telefon TEXT)")
    conn.commit()
    conn.close()

def insert(ime,prezime,tablice,telefon):
 
    conn = sqlite3.connect("zaposleni.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO data1 Values (NULL,?,?,?,?)",(ime,prezime,tablice,telefon))
    conn.commit()
    conn.close()

def view():

    conn = sqlite3.connect("zaposleni.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM data1")
    rows = cur.fetchall()
    conn.close()
    return rows

def search(ime="",prezime="",tablice="",telefon=""):

    conn = sqlite3.connect("zaposleni.db")
    cur = conn.cursor()
    cur.execute("Select * FROM data1 WHERE ime=? or prezime=? or tablice=? or telefon=?",(ime,prezime,tablice,telefon))
    rows = cur.fetchall()
    conn.close()
    return(rows)

def delete(id):

    conn = sqlite3.connect("zaposleni.db")
    cur  = conn.cursor()
    cur.execute("DELETE FROM data1 WHERE id=?",(id,))
    conn.commit()
    conn.close()

def update(id,ime,prezime,tablice,telefon):

    conn = sqlite3.connect("zaposleni.db")
    cur = conn.cursor()
    cur.execute("UPDATE data1 SET ime=?, prezime=?, tablice=?, telefon=? WHERE id=?",(ime,prezime,tablice,telefon,id))
    conn.commit()
    conn.close()

def delete_data():

    if os.path.exists("zaposleni.db"):
        os.remove("zaposleni.db")
    connect()


# tablica_unos='J68M017'
# # def read_from_db():
# cur.execute('SELECT tablice FROM data1')
# # data= cur.fetchall()
# # print(data)
# for row in cur.fetchall():
#     if tablica_unos in row:
#         print('True :D')
#         break
#     else:
#         print('Nije tu...')
        



# read_from_db()
connect()

 