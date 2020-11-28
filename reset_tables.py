import sqlite3 as sq
import parameters as P

par=P.Parameters()

con = sq.connect('Users.db')
c = con.cursor()

c.execute("DROP TABLE IF EXISTS Userlist")
c.execute("DROP TABLE IF EXISTS Parameters")

userlist_sql = """
CREATE TABLE Userlist (
    username text NOT NULL,
    password text NOT NULL,
    mode integer NOT NULL)
"""
c.execute(userlist_sql)
u_sql='''
    INSERT INTO Userlist (username, password, mode)
    VALUES(?, ?, 1)
'''
users = ['dave', 'alex', 'fei', 'christine', 'josh', 'mikha', 'GRamsay', 'ABokhari', 'LilJohn', 'Awatermelon']
passwords = ['321', '1', '2', '3', '4', '5', '9000', '1D042MD33K04', 'WHAT', 'juicy']

for i in range(10):
    c.execute(u_sql,(users[i], passwords[i]))

params_sql = """
CREATE TABLE Parameters (
    id integer PRIMARY KEY,
    mode integer NOT NULL,
    lrl integer NOT NULL,
    url integer NOT NULL,
    a_amp integer NOT NULL,
    v_amp integer NOT NULL,
    pw integer NOT NULL,
    a_sensi integer NOT NULL,
    v_sensi integer NOT NULL,
    rp integer NOT NULL,
    av_delay integer NOT NULL,
    act_thresh integer NOT NULL,
    react_t integer NOT NULL,
    res_fact integer NOT NULL,
    rec_t integer NOT NULL,
    msr integer NOT NULL,
    uid integer NOT NULL,
    FOREIGN KEY (uid) REFERENCES Userlist (oid))
    """
c.execute(params_sql)
p_sql= '''
    INSERT INTO Parameters (mode, lrl, url, a_amp, v_amp, pw, a_sensi, v_sensi, rp, av_delay, act_thresh, react_t, res_fact, rec_t, msr, uid) 
    VALUES (:mode, :lrl, :url, :a_amp, :v_amp, :pw, :a_sensi, :v_sensi, :rp, :av_delay, :act_thresh, :react_t, :res_fact, :rec_t, :msr, :uid)
    '''
for i in range(1,11):
    par_d = par.save(i)
    for j in range(1,12):
        par_d["mode"]=j
        c.execute(p_sql, par_d)

con.commit()
con.close()