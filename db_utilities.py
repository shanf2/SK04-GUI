import sqlite3 as sq

def conn(database):
    con = sq.connect(database)
    return con

def register(Data, name, password, nominal):
    c = Data.cursor()

    c.execute("INSERT INTO Userlist VALUES (?, ?, 1)", (name, password))
    c.execute("SELECT oid FROM Userlist WHERE username = ? AND password = ?", (name, password))

    row = c.fetchone()
    nominal["uid"] = row[0]

    p_sql= '''
    INSERT INTO Parameters (mode, lrl, url, a_amp, v_amp, pw, a_sensi, v_sensi, rp, av_delay, act_thresh, react_t, res_fact, rec_t, msr, uid) 
    VALUES (:mode, :lrl, :url, :a_amp, :v_amp, :pw, :a_sensi, :v_sensi, :rp, :av_delay, :act_thresh, :react_t, :res_fact, :rec_t, :msr, :uid)
    '''
    
    for j in range(1,12):
        nominal["mode"]=j
        c.execute(p_sql, nominal)
    Data.commit()

def fetch_users(Data):
    c = Data.cursor()#data cursor

    #fetch all of the data in database
    c.execute("SELECT *, oid FROM Userlist")
    records = c.fetchall()
    return records

def save_mode(Data, mode, uid):
    c = Data.cursor()

    c.execute("UPDATE Userlist SET mode = {} WHERE oid = {} ".format(mode, uid))
    Data.commit()

def delete(Data, user_id):
    c = Data.cursor()

    if(user_id != ""):
        c.execute("DELETE from Userlist WHERE oid =?", (user_id,))
        c.execute("DELETE from Parameters WHERE uid =?", (user_id,))

    Data.commit()

def save_params(Data, par):
    c = Data.cursor()
    for k, v in par.items():
        if(k != "mode" and k != "uid"):
            sql= "UPDATE Parameters SET {} = {} WHERE uid = {} AND mode = {}".format(k, v, par["uid"], par["mode"])
            c.execute(sql, par)
    Data.commit()

def load_params(Data, uid, mode):
    c = Data.cursor()
    d={}
    sql = "SELECT * FROM Parameters WHERE uid = ? AND mode = ?"
    c.row_factory = sq.Row
    c.execute(sql, (uid, mode))

    vals = c.fetchone()
    i=1
    for v in vals.keys():
        if(v!='id'):
            d[v]=vals[i]
            i+=1
    return d