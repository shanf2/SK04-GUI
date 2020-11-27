import sqlite3 as sq

def conn(database):
    con = sq.connect(database)
    return con

def fetch_users(Data):
    c = Data.cursor()#data cursor

    #fetch all of the data in database
    c.execute("SELECT *, oid FROM address")
    records = c.fetchall()
    Data.close()
    return records

def delete(Data, user_id):
    c = Data.cursor()

    if(user_id != ""):
	    c.execute("DELETE from address WHERE oid =" + user_id)
    Data.commit()
    Data.close()

def register(Data, name, password):
    c = Data.cursor()

    c.execute("INSERT INTO address VALUES (:username, :password)", \
             { 'username': name, 'password': password })
    Data.commit()
    Data.close()